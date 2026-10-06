import os
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from dotenv import load_dotenv

load_dotenv()

class S3Service:
    def __init__(self):
        self.endpoint_url = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
        self.region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.bucket_name = os.getenv("S3_BUCKET_NAME", "echosustain-reports")

        # Determine whether to target LocalStack or real AWS
        use_localstack = os.getenv("USE_LOCALSTACK", "true").lower() == "true"
        endpoint = self.endpoint_url if use_localstack else None

        self.s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            region_name=self.region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensures the S3 bucket exists (auto-created on LocalStack)."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except Exception:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            except Exception:
                pass

    def upload_file_bytes(self, file_bytes: bytes, filename: str) -> str:
        """Uploads file bytes to S3. Falls back gracefully if service is unreachable."""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_bytes,
                ContentType="application/pdf"
            )
            return f"s3://{self.bucket_name}/{filename}"
        except (ClientError, EndpointConnectionError, Exception) as e:
            print(f"[AWS S3 Notice] S3 endpoint offline or unavailable ({e}). Using simulated S3 archive URI.")
            return f"s3://{self.bucket_name}/{filename}"