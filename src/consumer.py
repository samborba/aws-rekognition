import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from processor import Processor


load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('REGION_NAME')

AWS_KINESISVIDEO_ARN = os.getenv('AWS_KINESISVIDEO_ARN')
AWS_KINESISVIDEO_NAME = os.getenv('AWS_KINESISVIDEO_NAME')
IAM_REKOGNITION_ROLE_ANR = os.getenv('IAM_REKOGNITION_ROLE_ANR')
AWS_KINESISDATA_ARN = os.getenv('AWS_KINESISDATA_ARN')
AWS_KINESISDATA_NAME = os.getenv('AWS_KINESISDATA_NAME')

COLLECTION_NAME = os.getenv('COLLECTION_NAME')
PROCESSOR_NAME = os.getenv('PROCESSOR_NAME')


def inital_config():
    """Cria sessão com o client da AWS para usar seus serviços."""

    try:
        session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=REGION_NAME
                                )
        return session
    except Exception as error:
        print(f'Erro ao connectar: {error}')


def collection_initialize():
    """
    Cria uma collection que armazena as faces detectadas.
    Pode-se usar as informações faciais que estão armazenadas
    em uma collection para procurar por faces conhecidas em
    imagens, videos armazenados e streaming de vídeo.
    """

    try:
        print(f'Criando {COLLECTION_NAME} collection...')
        rekognition_client = inital_config().client('rekognition')
        response = rekognition_client.create_collection(CollectionId=COLLECTION_NAME)

        print('Criado com sucesso.')
        print('Collection ARN: ' + response['CollectionArn'])
        print(response)
    except ClientError as error:
        print(f'Erro ao criar {COLLECTION_NAME} collection: {error}')


# def collection_delete(collection_name=KEY_COLLECTION_ID):
#     """Exclui uma collection dado seu nome."""
#     try:
#         print(f'Excluindo {collection_name} collection...')
#         response = REKOG_CLIENT.delete_collection(
#             CollectionId=collection_name
#         )
#         print('Status code: ' + str(response['StatusCode']))
#     except Exception as error:
#         print(f'Falha ao excluir {collection_name}: {error}')


# def processor_initialize():
#     """
#     Cria um processor de fluxo do Rekognition que detecta
#     e reconhece rostos em um streaming de vídeo.
#     Fornece Input que se trata de quem vai fornecer a fonte de vídeo,
#     e o Output, onde irá ser armazenado as análises dos resultados.
#     """

#     try:
#         print('Criando processor...')
#         REKOG_CLIENT.create_stream_processor(
#             Input={
#                 'KinesisVideoStream': {
#                     'Arn': KEY_AWS_VIDEO_ARN
#                 }
#             },
#             Output={
#                 'KinesisDataStream': {
#                     'Arn': KEY_AWS_DATA_ARN
#                 }
#             },
#             Name=KEY_PROCESSOR_NAME,
#             Settings={
#                 'FaceSearch': {
#                     'CollectionId': COLLECTION_NAME,
#                     'FaceMatchThreshold': 70.0
#                 }
#             },
#             RoleArn=KEY_ROLE_ARN
#         )

#         processor_response = REKOG_CLIENT.start_stream_processor(
#             Name=KEY_PROCESSOR_NAME
#         )
#         print('Criado com sucesso!')

#         return processor_response
#     except ClientError as error:
#         print(error)


# def processor_stop(name=KEY_PROCESSOR_NAME):
#     """Para um determinado processor dado seu nome."""

#     try:
#         rekognition_client = inital_config().client('rekognition')

#         print('Parando processor...')
#         rekognition_client.stop_stream_processor(
#             Name=name
#         )
#         print('Processor {name} foi parado com sucesso.')
#     except Exception as error:
#         print(f'Erro ao parar processor: {error}')


# def processor_delete(name=KEY_PROCESSOR_NAME):
#     """Deleta um determiando processor dado seu nome."""

#     try:
#         rekognition_client = inital_config().client('rekognition')
#         print('Excluindo processor...')

#         rekognition_client.delete_stream_processor(
#             Name=name
#         )
#         print(f'Processor {name} exluído.')
#     except Exception as error:
#         print(error)


# def processor_status():
#     try:
#         rekognition_client = inital_config().client('rekognition')

#         response = rekognition_client.describe_stream_processor(
#             Name=PROCESSOR_NAME
#         )
#     except Exception as error:
#         print(error)


if __name__ == "__main__":
    collection_initialize()
