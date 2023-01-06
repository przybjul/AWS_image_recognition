from typing import List, Optional

import boto3
import psycopg2
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from orm import get_image_description, get_image_transcription
from pydantic import BaseModel

S3_BUCKET_NAME = "image-recognition-1"
S3_BUCKET_NAME2 = "image-transcribe-1"


class PhotoModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str
    is_deleted: Optional[bool] = None
    description: str


app = FastAPI(debug=True)
#Middleware do autoryzacji
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
async def check_status():
    return "Hello World!"


@app.get("/photos", response_model=List[PhotoModel])
async def get_all_photos():
    # Connect to our database
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="localhost",
        port=5432,
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM photo ORDER BY id DESC")
    rows = cur.fetchall()
    formatted_photos = []
    for row in rows:
        print(row[0])
        photo_description = get_image_description(photo=row[0])
        formatted_photos.append(
            PhotoModel(
                id=row[3],
                photo_name=row[0],
                photo_url=row[1],
                is_deleted=row[2],
                description=photo_description,
            )
        )
        break
    print(f"{formatted_photos=}")
    cur.close()
    conn.close()
    return formatted_photos


@app.post("/photos", status_code=201)
async def add_photo(file: UploadFile):
    print("Create endpoint hit!!")
    print(file.filename)
    print(file.content_type)

    # Upload file to AWS S3
    s3 = boto3.resource(
        "s3",
        aws_access_key_id="",
        aws_secret_access_key="",
    )
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})

    uploaded_file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"

    # Store URL in database
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO photo (photo_name, photo_url) VALUES ('{file.filename}', '{uploaded_file_url}' )"
    )
    conn.commit()
    cur.close()
    conn.close()


# ----------------------------------------------------------------------------------------------------------------------------------


@app.post("/transcription", status_code=201)
async def add_photo(file: UploadFile):
    print("Create endpoint hit!!")
    print(file.filename)
    print(file.content_type)

    # Upload file to AWS S3
    s3 = boto3.resource(
        "s3",
        aws_access_key_id="",
        aws_secret_access_key="",
    )
    bucket = s3.Bucket(S3_BUCKET_NAME2)
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})

    uploaded_file_url = f"https://{S3_BUCKET_NAME2}.s3.amazonaws.com/{file.filename}"

    # Store URL in database
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO transcribe (photo_name, photo_url) VALUES ('{file.filename}', '{uploaded_file_url}' )"
    )
    conn.commit()
    cur.close()
    conn.close()


@app.get("/transcription", response_model=List[PhotoModel])
async def get_all_photos():
    # Connect to our database
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="localhost",
        port=5432,
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM transcribe ORDER BY id DESC")
    rows = cur.fetchall()
    formatted_photos = []
    for row in rows:
        photo_description = get_image_transcription(photo=row[0])
        formatted_photos.append(
            PhotoModel(
                id=row[3],
                photo_name=row[0],
                photo_url=row[1],
                is_deleted=row[2],
                description=photo_description,
            )
        )
        break
    cur.close()
    conn.close()
    return formatted_photos


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=False)
