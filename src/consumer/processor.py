import logging
import os
import boto3

_AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
_AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
_AWS_REGION_KEY = os.environ.get('AWS_REGION_KEY')


class Processor:
    """
    Classe responsável pelo Processor da aplicação.
    Ele é responsável por fazer o intermédio entre o Kinesis Video Streams
    e Kinesis Data Streams.
    """
    def __init__(self, input_location, output_location,
                 name, collection_id, rolearn):
        self.input_location = input_location
        self.output_location = output_location
        self.name = name
        self.collection_id = collection_id
        self.rolearn = rolearn

        session = boto3.Session(aws_access_key_id=_AWS_ACCESS_KEY, aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                                region_name=_AWS_REGION_KEY)
        client = session.client('rekognition')
        self._rekognition_client = client

    def create(self):
        """Criação do processor."""
        try:
            logging.info('Criando %s processor.', self.name)

            self._rekognition_client.create_stream_processor(
                Input={
                    'KinesisVideoStream': {
                        'Arn': self.input_location
                    }
                },
                Output={
                    'KinesisDataStream': {
                        'Arn': self.output_location
                    }
                },
                Name=self.name,
                Settings={
                    'FaceSearch': {
                        'CollectionId': self.collection_id,
                        'FaceMatchThreshold': 70.0
                    }
                },
                RoleArn=self.rolearn
            )
            logging.info('Processaor %s criado com Sucesso!', self.name)
        except Exception as error:
            logging.error(error)

    def initialize(self):
        """
        Inicialização do processor.
        """
        try:
            logging.info('Inicializando %s processor.', self.name)

            self._rekognition_client.start_stream_processor(Name=self.name)

            logging.info('Incializado com sucesso!')
        except Exception as error:
            logging.error(error)

    def stop(self):
        """
        Para o processor.
        """
        try:
            logging.info('Parando %s processor', self.name)

            self._rekognition_client.stop_stream_processor(Name=self.name)

            logging.info('Parado com sucesso')
        except Exception as error:
            logging.error(error)

    def delete(self):
        """
        Deleta o processor.
        """
        try:
            logging.info('Deletando %s processor', self.name)

            self._rekognition_client.delete_stream_processor(Name=self.name)

            logging.info('Deletado com sucesso.')
        except Exception as error:
            logging.error(error)

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
            logging.error(error)
