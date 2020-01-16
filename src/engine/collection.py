import logging
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

_AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
_AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
_AWS_REGION_KEY = os.getenv('REGION_NAME')


class CollectionManager:
    """
    Cria uma Collection que é responsável por armazenar a
    coleção de faces para serem reconehcidas pelo Rekognition.
    """

    def __init__(self):
        session = boto3.Session(aws_access_key_id=_AWS_ACCESS_KEY, aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                                region_name=_AWS_REGION_KEY)

        r_client = session.client('rekognition')
        s_client = session.client('s3')

        # Cria conexão com o rekognition
        self._rekognition_client = r_client

        # Cria conexão com o S3
        self._s3_client = s_client

    def create(self, collection_id):
        """
        Cria uma nova collection.
        """
        try:
            print(f'Criando {collection_id} collection.')

            response = self._rekognition_client.create_collection(
                CollectionId=collection_id
            )

            print('Collection criada com sucesso.')
            print('\t #@#@# ' + response.get('StatusCode'))
            print('\t #@#@# ' + response.get('CollectionArn'))
        except Exception as error:
            print(error)

    def remove_collection(self, collection_id):
        """
        Remove collection.
        :param collection_id: String CollectionId referente à collection que será removida.
        """
        try:
            print(f'Deleteando {collection_id} collection.')
            response = self._rekognition_client.delete_collection(CollectionId=collection_id)
            status_code = response.get('StatusCode')

            if status_code == 200:
                print('Collection excluida com sucesso.')
        except Exception as error:
            print(error)

    def get_list(self):
        """
        Consulta todas as collections já criadas.
        :return: List lista de collectios da AWS.
        """
        try:
            print('Retornando todas as collections.')
            response = self._rekognition_client.list_collections(MaxResults=5)
            collections_ids = response.get('CollectionIds')

            return collections_ids
        except Exception as error:
            print(error)

    def index_face(self, collection, photo):
        pass
