import boto3


def get_image_description(photo: str):
    client = boto3.client(
        "rekognition",
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name="us-east-1",
    )
    # rozpoznanie twarzy
    response = client.detect_faces(
        Image={"S3Object": {"Bucket": "image-recognition-1", "Name": photo}},
        Attributes=["ALL"],
    )

    for key, value in response.items():
        if key == "FaceDetails":
            for people_att in value:
                gender = str(people_att["Gender"]["Value"])
                low_age_range = str(people_att["AgeRange"]["Low"])
                high_age_range = str(people_att["AgeRange"]["High"])
                smile = str(people_att["Smile"]["Value"])
                if smile == "True":
                    is_smiling = "is smiling."
                else:
                    is_smiling = "is not smiling."
                emotion = people_att["Emotions"][0]["Type"]
                # print("This person is "+gender+". Age of this person is in range from "+low_age_range+" to " + high_age_range + " years old. This person "+is_smiling)
                string = (
                    "This person is "
                    + gender
                    + ". Age of this person is in range from "
                    + low_age_range
                    + " to "
                    + high_age_range
                    + " years old. This person "
                    + is_smiling
                    + " Emotions: "
                    + emotion
                )
    return string


def get_image_transcription(photo: str):
    # S3 Bucket Data
    s3BucketName = "image-transcribe-1"
    # Amazon Textract client
    textractmodule = boto3.client(
        "textract",
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name="us-east-1",
    )

    response = textractmodule.detect_document_text(
        Document={"S3Object": {"Bucket": s3BucketName, "Name": photo}}
    )
    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text = text + item["Text"] + " "
    return text
