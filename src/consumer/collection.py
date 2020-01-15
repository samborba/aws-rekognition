import logging
import os
import boto3

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION_KEY = os.environ.get('AWS_REGION_KEY')


class CollectionManager:
    """
    Cria uma Collection que é responsável por armazenar a
    coleção de faces para serem reconehcidas pelo Rekognition.
    """

    def __init__(self, collection_id):
        self.collection_id = collection_id
        self.collection_arn = None
        self.face_count = None
        self.creation_timestamp = None

        session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=AWS_REGION_KEY)

        r_client = session.client('rekognition')
        s_client = session.client('s3')

        # Cria conexão com o rekognition
        self._rekognition_client = r_client

        # Cria conexão com o S3
        self._s3_client = s_client

    def create(self):
        """
        Cria uma nova collection.
        """
        try:
            logging.info('Criando %s collection', self.collection_id)

            response = self._rekognition_client.create_collection(
                CollectionId=self.collection_id
            )

            logging.info('Collection criada com sucesso.')
            logging.info(response.get('StatusCode'))
            logging.info(response.get('CollectionArn'))
        except Exception as error:
            logging.error(error)

    def remove_collection(self, collection_id):
        """
        Remove collection.
        :param collection_id: String CollectionId referente à collection que será removida.
        """
        try:
            logging.info('Deleteando %s collection', collection_id)
            response = self._rekognition_client.delete_collection(CollectionId=collection_id)
            status_code = response.get('StatusCode')

            if status_code == 200:
                logging.info('Collection excluida com sucesso.')
        except Exception as error:
            logging.error(error)

    def get_list(self):
        """
        Consulta todas as collections já criadas.
        :return: List lista de collectios da AWS.
        """
        try:
            logging.info('Retornando todas as collections.')
            response = self._rekognition_client.list_collections(MaxResults=5)
            collections_ids = response.get('CollectionIds')

            return collections_ids
        except Exception as error:
            logging.error(error)

    def index_face(self, collection, photo):
        pass
