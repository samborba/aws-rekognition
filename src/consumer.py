import os
from dotenv import load_dotenv

from engine.processor import Processor
from engine.collection import CollectionManager

load_dotenv()

PROCESSOR_NAME = os.getenv('PROCESSOR_NAME')
# Caso já tenha alguma collection, mude o valor de "COLLECTION_ID" para o nome dela.
COLLECTION_ID = os.getenv('COLLECTION_ID')

AWS_KINESISVIDEO_ARN = os.getenv('AWS_KINESISVIDEO_ARN')
AWS_DATASTREAMS_ARN = os.getenv('AWS_DATASTREAMS_NAME')

AWS_KVS_ROLE_ARN = os.getenv('AWS_KVS_ROLE_ARN')


def building_engines(collection_id=COLLECTION_ID):
    """
    Cria o processor responsável por manter o intermédio entre o Kinesis Video Stream e
    o Kinesis Data Streams, e cria a collection que irá armazenar e indexar as faces
    que serão reconhecidas pelo Rekognition.

    Caso já tenha uma collection e queira usa-la, basta mudar o
    valor do parametro para o Id dela. (Ela precisar estar populada, caso contrário,
    não irá detectar as pessoas na análise.) 
    """
    try:        
        collection = CollectionManager()

        # Verifica se é a collection default do projeto, se for, irá popular
        if collection_id == COLLECTION_ID:
            # Verifica se collection existe, caso contrário, cria uma nova
            if COLLECTION_ID not in collection.get_list():
                # Popula collection com as faces em '../resources'
                collection.index_face(collection_id)
            else:
                print(f'Collection {collection_id} já está criada.')
        else:
            print(f'Usando collection {collection_id} já criada pelo usuário.')

        # Cria processor
        processor = Processor(PROCESSOR_NAME, COLLECTION_ID)
        processor.create()
        processor.initialize()
    except Exception as error:
        print(error)


def consuming_analysis():
    """
    Consome a saída de dados gerados pelo Kinesis Data Streams.
    """
    # 1. Configurar boto3
    # 2. Consumir ánalise
    # 3. Assim que a ánalise for parada, parar processor e exclui-lo
    pass


def main():
    building_engines()
    consuming_analysis()


if __name__ == "__main__":
    main()
