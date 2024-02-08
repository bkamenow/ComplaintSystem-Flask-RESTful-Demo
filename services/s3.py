import boto3
from botocore.exceptions import ClientError


from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    def __init__(self):
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY"),
            aws_secret_access_key=config("AWS_SECRET"),
        )

    def upload_photo(self, file_path, file_name, bucket=None, region=None):
        if not bucket:
            bucket = config("AWS_BUCKET")
        if not region:
            region = config("AWS_REGION")

        try:
            self.s3.meta.client.upload_file(file_path, bucket, file_name)

            return f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}"
        except ClientError:
            raise InternalServerError("S3 is not available at the moment")
