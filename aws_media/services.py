import boto3
import magic
from fastapi import HTTPException

# region AWS S3
# create a session with AWS using boto3 library in IAM user
session = boto3.Session(
    aws_access_key_id="AKIAQLSZYWF72GE6SHWL",
    aws_secret_access_key="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",
)

KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif"
}

AWS_BUCKET = "ems-project-media"
s3 = session.resource("s3")
bucket = s3.Bucket(AWS_BUCKET)


async def s3_upload(contents: bytes, key: str):
    print(f"Uploading to S3")
    bucket.put_object(Key=key, Body=contents)


async def upload_file(file):
    if not file:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "detail": "No file uploaded",
            "data": None
        })


    contents = await file.read()
    file_size = len(contents)

    if not 0 < file_size < 10 * MB:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "detail": f"File size is too large or too small (0 < file_size < 10 MB)",
            "data": None
        })

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "detail": f"File type {file_type} is not supported",
            "data": None
        })

    # save to S3 bucket with photo
    print("file is ", file.filename.split(".")[0])
    file_name = f"{file.filename.split('.')[0]}.{SUPPORTED_FILE_TYPES[file_type]}"
    await s3_upload(contents=contents, key=file_name)

    #     get the url of the image
    return f"https://{AWS_BUCKET}.s3.amazonaws.com/{file_name}"


async def change_url(urls: str, to_list: bool):
    if urls is None:
        return []
    if to_list:
        return urls.split(",")
    else:
        return ",".join(urls)

# endregion
