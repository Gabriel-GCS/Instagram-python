import boto3
from botocore.exceptions import ClientError
from decouple import config


class AWSProvider:

    def upload_file_s3(self, save_route, file_route, bucket='instagram=python'):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_private_access_key_id=config('AWS_SECRET_KEY')
        )

        try:
            response = s3_client.upload_file(file_route, bucket, Key=save_route)
            print(response)
        except ClientError as error:
            print(error)
            return False
