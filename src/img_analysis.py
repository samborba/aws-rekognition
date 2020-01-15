import os
import boto3
from dotenv import load_dotenv

load_dotenv()

KEY_S3_BUCKET = os.getenv('KEY_S3_BUCKET')
KEY_AWS_ACCESS = os.getenv('KEY_AWS_ACCESS')
KEY_AWS_SECRET_ACCESS = os.getenv('KEY_AWS_SECRET_ACCESS')
KEY_REGION_NAME = os.getenv('KEY_REGION_NAME')
KEY_AWS_SESSION_ACCESS = os.getenv('KEY_AWS_SESSION_ACCESS')
MAX_LABELS = 10

def inital_config():
    try:
        session = boto3.Session(aws_access_key_id=KEY_AWS_ACCESS,
                                aws_secret_access_key=KEY_AWS_SECRET_ACCESS,
                                region_name=KEY_REGION_NAME,
                                aws_session_token=KEY_AWS_SESSION_ACCESS
                                )
        return session
    except Exception as error:
        print(f'Erro ao connectar: {error}')

def local_file(photo):
    """Faz análise de imagem local"""
    resource = inital_config()
    client = resource.client('rekognition')
    with open(f"./assets/{photo}", 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=MAX_LABELS)

    print(f'Labels detectadas na imagem {photo}: ')
    for label in response['Labels']:
        print(label['Name'] + ': ' + str(label['Confidence']))

    return len(response['Labels'])


def bucket_file(photo):
    """Faz análise de imagem no S3 Bucket da Amazon"""
    resource = inital_config()
    client = resource.client('rekognition')
    response = client.detect_labels(Image={'S3Object': {'Bucket': KEY_S3_BUCKET, 'Name': photo}}, 
                                    MaxLabels=MAX_LABELS)

    print(f'Labels detectadas na imagem {photo} do Bucket {KEY_S3_BUCKET}: ')
    for label in response['Labels']:
        print(label['Name'] + ': ' + str(label['Confidence']))

    return len(response['Labels'])
