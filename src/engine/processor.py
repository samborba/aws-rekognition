import logging
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

_AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
_AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
_AWS_REGION_KEY = os.getenv('REGION_NAME')
_AWS_KVS_ROLE_ARN = os.getenv('AWS_KVS_ROLE_ARN')

_KINESISVIDEO_ARN = os.getenv('AWS_KINESISVIDEO_ARN')
_KINESISDATA_ARN = os.getenv('AWS_DATASTREAMS_ARN')


class Processor:
    """
    Classe responsável pelo Processor da aplicação.
    Ele é responsável por fazer o intermédio entre o Kinesis Video Streams
    e Kinesis Data Streams.
    """
    def __init__(self, name, collection_id):
        self.name = name
        self.collection_id = collection_id

        session = boto3.Session(aws_access_key_id=_AWS_ACCESS_KEY, aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                                region_name=_AWS_REGION_KEY)
        client = session.client('rekognition')
        self._rekognition_client = client

    def create(self):
        """Criação do processor."""
        try:
            print(f'Criando {self.name} processor.')

            self._rekognition_client.create_stream_processor(
                Input={
                    'KinesisVideoStream': {
                        'Arn': _KINESISVIDEO_ARN
                    }
                },
                Output={
                    'KinesisDataStream': {
                        'Arn': _KINESISDATA_ARN
                    }
                },
                Name=self.name,
                Settings={
                    'FaceSearch': {
                        'CollectionId': self.collection_id,
                        'FaceMatchThreshold': 70.0
                    }
                },
                RoleArn=_AWS_KVS_ROLE_ARN
            )
            print(f'Processaor {self.name} criado com Sucesso!')
        except Exception as error:
            print(error)

    def initialize(self):
        """
        Inicialização do processor.
        """
        try:
            print(f'Inicializando {self.name} processor.')
            self._rekognition_client.start_stream_processor(Name=self.name)

            print('Incializado com sucesso!')
        except Exception as error:
            print(error)

    def stop(self):
        """
        Para o processor.
        """
        try:
            print(f'Parando {self.name} processor.')
            self._rekognition_client.stop_stream_processor(Name=self.name)

            print('Parado com sucesso')
        except Exception as error:
            print(error)

    def delete(self):
        """
        Deleta o processor.
        """
        try:
            print(f'Deletando {self.name} processor.')
            self._rekognition_client.delete_stream_processor(Name=self.name)

            print('Deletado com sucesso.')
        except Exception as error:
            print(error)

    def status(self):
        """
        Retorna o status do Precessor:
        STOPPED | STARTING | RUNNING | FAILED | STOPPING'.
        :return: String retorna htpp code.
        """
        try:
            response = self._rekognition_client.delete_stream_processor(Name=self.name)
            return response.get('Status')
        except Exception as error:
            print(error)
