import boto3
import json

AWS_ACCESS_KEY = "YOUR_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_SECRET_KEY"
BUCKET_NAME = "YOUR_BUCKET"

def fetch_papers_from_s3():

    papers = []

    try:

        print("Connecting to AWS S3...")

        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        if "Contents" not in response:
            print("No files found in S3 bucket")
            return papers

        print(f"Total files found in bucket: {len(response['Contents'])}")

        for obj in response["Contents"]:

            key = obj["Key"]

            if key.endswith(".json"):

                print(f"Fetching file: {key}")

                file = s3.get_object(Bucket=BUCKET_NAME, Key=key)

                data = json.loads(file["Body"].read().decode("utf-8"))

                data["source"] = "AWS S3"

                papers.append(data)

        print(f"S3 papers loaded successfully: {len(papers)}")

    except Exception as e:

        print("S3 ERROR:", str(e))

    return papers