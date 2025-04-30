import json
import os
import sys

from echoss_fileformat import FileUtil

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('../'))))
from echoss_storage import S3ResourceHandler


env = 'develop'
env_config = FileUtil.dict_load('env_config.yaml')[env]
s3_config = env_config['s3']

test_s3 = S3ResourceHandler(s3_config)

bucket_list = test_s3.get_bucket_list(include_date=True)

object_json_list = test_s3.get_object_list(s3_config['bucket'], "", pattern=".json")

for  obj in object_json_list:
    obj_fileview = test_s3.get_object_file(s3_config['bucket'], obj)
    json_data = obj_fileview.as_json()
    print(f"{json_data=}")

pass




