import boto3
from botocore.exceptions import ClientError
from decouple import config


class AWSProvider:

    def upload_file_s3(self, save_route, file_route, bucket='instagram-python'):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY')
        )
        try:
            s3_client.upload_file(file_route, bucket, Key=save_route)
            url = s3_client.generate_presigned_url(
                'get_object',
                ExpiresIn=0,
                Params={'Bucket': bucket, 'Key': save_route}
            )
            return str(url).split('?')[0]
        except ClientError as error:
            print(error)
            return False
