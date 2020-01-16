import os
from dotenv import load_dotenv

from engine.processor import Processor
from engine.collection import CollectionManager

load_dotenv()

PROCESSOR_NAME = os.getenv('PROCESSOR_NAME')
COLLECTION_ID = os.getenv('COLLECTION_ID')

AWS_KINESISVIDEO_ARN = os.getenv('AWS_KINESISVIDEO_ARN')
AWS_DATASTREAMS_ARN = os.getenv('AWS_DATASTREAMS_NAME')

AWS_KVS_ROLE_ARN = os.getenv('AWS_KVS_ROLE_ARN')

if __name__ == "__main__":
    # collection = CollectionManager()
    # collection.create(COLLECTION_ID)
    processor = Processor(PROCESSOR_NAME, COLLECTION_ID)

    processor.create()
    processor.initialize()
