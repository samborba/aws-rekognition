import pickle
import os
from datetime import datetime
from multiprocessing import Pool
import cv2
import boto3

CAMERA_INDEX = 0
CAPTURE_RATE = 100

KEY_AWS_DATA_STREAM = os.getenv('KEY_AWS_DATA_STREAM')

def encode_and_send_frame(frame, frame_count):
    """
    A função VideoCapture do OpenCV retorna bytes de imagens "raw"
    que no caso não são .jpg. A função encode_and_send_frame
    converte as imagens recebidas e envia para o Amazon Kinesis Data Stream.
    """
    kinesis_client = boto3.client('kinesis')

    try:
        retval, buff = cv2.imencode(".jpg", frame) # compacta a imagem e armazena no buffer

        img_bytes = bytearray(buff)  # transforma o buffer em um array de bytes

        # horário
        utc_dt = pytz.utc.localize(datetime.now())
        now_ts_utc = (utc_dt - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

        # cria uma estrutura com os dados do frame para serem enviados ao AWS Kinesis Data Stream
        frame_package = {
            'ApproximateCaptureTime': now_ts_utc,
            'FrameCount': frame_count,
            'ImageBytes': img_bytes
        }

        # Registra os dados (frames) no AWS Kinesis Data Stream
        kinesis_client.put_record(StreamName=KEY_AWS_DATA_STREAM,
                                  Data=pickle.dumps(frame_package), # faz a serialização do frame
                                  PartitionKey='partitionkey')

    except Exception as error:
        print(f'Aconteceu um erro: {error}')


def webcam_producer():
    """
    Inicia conexão com a webcam passada como argumento no método VideoCapture.
    A cada frame, é chamada a função encode_and_send_frame para a codificação e envio ao Kinesis.
    Esta função é executada paralelamente utilizando a biblioteca multiprocessing.
    """

    cap = cv2.VideoCapture(0)
    pool = Pool(processes=3)

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if ret is False:
            break

        if frame_count % CAPTURE_RATE == 0:
            result = pool.apply_async(encode_and_send_frame, (frame,
                                                              frame_count))

        frame_count += 1

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
