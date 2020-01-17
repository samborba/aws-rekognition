import os
import json
from dotenv import load_dotenv
import boto3

from engine.processor import Processor
from engine.collection import CollectionManager

load_dotenv()

PROCESSOR_NAME = os.getenv('PROCESSOR_NAME')
# Caso já tenha alguma collection, mude o valor de "COLLECTION_ID" para o nome dela.
COLLECTION_ID = os.getenv('COLLECTION_ID')

AWS_KINESISVIDEO_ARN = os.getenv('AWS_KINESISVIDEO_ARN')
AWS_DATASTREAMS_ARN = os.getenv('AWS_DATASTREAMS_NAME')

AWS_KVS_ROLE_ARN = os.getenv('AWS_KVS_ROLE_ARN')


def start_analysis(collection_id=COLLECTION_ID):
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

    kinesis_data_streams = boto3.client('kinesis')

    shardId = kinesis_data_streams.describe_stream(
        StreamName=AWS_DATASTREAMS_ARN)['StreamDescription']['Shards'][0]['ShardId']
    shardIterator = kinesis_data_streams.get_shard_iterator(StreamName=AWS_DATASTREAMS_ARN,
                                                            ShardId=shardId,
                                                            ShardIteratorType='TRIM_HORIZON')['ShardIterator']

    try:
        while True:
            records = kinesis_data_streams.get_records(ShardIterator=shardIterator, limit=1)
            shardIterator = records['NextShardIterator']

            if len(records['Records'] > 0):
                data = json.loads(recs['Records'][0]['Data'])
                if len(data['FaceSearchResponse']) > 0:
                    for faceSearchResponse in data['faceSearchResponse']:
                        if len(faceSearchResponse['MatchedFaces']) > 0:
                            for face in faceSearchResponse['MatchedFaces']:
                                name = face['Face']['ExternalImageId']
                                confidence = face['Face']['Confidence']
                                print(f'Rosto reconhecido: {nome}\nConfiança: {confidence}')

    except KeyboardInterrupt:
        print('Parando análise...')
        processor.stop()
        processor.delete()


def main():
    start_analysis()


if __name__ == "__main__":
    main()
