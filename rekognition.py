import csv
import boto3

with open('new_user_credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

photo = 'zdj.jpg'

client = boto3.client('rekognition', aws_access_key_id = "AKIAY7OFF5K7MJPS6TD4", aws_secret_access_key = "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", region_name='us-west-2')

# with open(photo, 'rb') as source_image:
#     source_bytes = source_image.read()

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

#rozpoznanie twarzy
response = client.detect_faces(Image={'S3Object':{
    "Bucket":"image-recognition-1",
    "Name":photo
    }},Attributes=['ALL'])

for key, value in response.items():
    if key == 'FaceDetails':
        for people_att in value:
            gender = str(people_att["Gender"]["Value"])
            low_age_range = str(people_att["AgeRange"]["Low"])
            high_age_range = str(people_att["AgeRange"]["High"])
            smile = people_att["Gender"]["Value"]
            if smile:
                is_smiling = "is smiling."
            else:
                is_smiling = "is not smiling."
            # print("This person is "+gender+". Age of this person is in range from "+low_age_range+" to " + high_age_range + " years old. This person "+is_smiling)
            print(people_att)
            print("_________")
# print(response)
