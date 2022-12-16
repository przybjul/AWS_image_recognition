import csv
import boto3

with open('new_user_credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

photo = 'beyonce.jpg'

client = boto3.client('rekognition', aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key, region_name='us-west-2')

with open(photo, 'rb') as source_image:
    source_bytes = source_image.read()

# response = client.detect_labels(Image={'Bytes':source_bytes}, MaxLabels = 2, MinConfidence=95)

#rozpoznanie rodzaju obiektu
response = client.detect_labels(Image={'S3Object':{
    "Bucket":"image-recognition-1",
    "Name":photo
    }}, MaxLabels = 2, MinConfidence=95)

#moderacja - treści niewłaściwe takie jak nudity
response = client.detect_moderation_labels(Image={'S3Object':{
    "Bucket":"image-recognition-1",
    "Name":photo
    }},MinConfidence=90)

print(response)
