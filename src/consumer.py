import os
from dotenv import load_dotenv

from engine.processor import Processor
from engine.collection import CollectionManager

load_dotenv()

PROCESSOR_NAME = os.getenv('PROCESSOR_NAME')
# Caso já exista alguma collection, mude o valor de "COLLECTION_ID" para o nome dela.
COLLECTION_ID = os.getenv('COLLECTION_ID')

AWS_KINESISVIDEO_ARN = os.getenv('AWS_KINESISVIDEO_ARN')
AWS_DATASTREAMS_ARN = os.getenv('AWS_DATASTREAMS_NAME')

AWS_KVS_ROLE_ARN = os.getenv('AWS_KVS_ROLE_ARN')


def building_engines():
    """
    Cria o processor responsável por manter a ligação entre o Kinesis Video Stream e
    o Kinesis Data Streams, e cria a collection que irá armazenar e indexar as faces
    que serão reconhecidas pelo Rekognition.
    """
    try:
        # 1. Criar Collection
        collection = CollectionManager()
        collection.create(COLLECTION_ID)

        # 2. Fazer indexação das faces - TO DO
        collection.index_face()

        # 3. Criar processor
        processor = Processor(PROCESSOR_NAME, COLLECTION_ID)
        processor.create()
        processor.initialize()
    except Exception as error:
        print(error)


def logger_setup():
    # Precisa ver se essa função fica aqui ou no ./utils/logger
    # 1. Criar pasta de log
    # 2. Criar arquivo de log
    pass


def consuming_analysis():
    """
    Consome a saída de dados gerados pelo Kinesis Video Streams.
    """
    # 1. Configurar boto3
    # 2. Consumir ánalise
    pass


def main():
    building_engines()
    logger_setup()


if __name__ == "__main__":
    main()
