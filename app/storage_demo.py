import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

root = Path(__file__).resolve().parents[1]
load_dotenv(root / '.env')

client = boto3.client(
    's3',
    endpoint_url=os.environ['STORAGE_ENDPOINT'],
    aws_access_key_id=os.environ['STORAGE_ACCESS_KEY'],
    aws_secret_access_key=os.environ['STORAGE_SECRET_KEY'],
    region_name=os.environ['STORAGE_REGION'],
)
bucket = os.environ['STORAGE_BUCKET']

# Создание bucket для локального учебного хранилища Moto.
try:
    client.head_bucket(Bucket=bucket)
except ClientError as error:
    if error.response['Error']['Code'] != '404':
        raise
    client.create_bucket(Bucket=bucket)

source = root / 'uploads' / 'test.txt'
downloaded = root / 'uploads' / 'downloaded_test.txt'
client.upload_file(str(source), bucket, 'lab9/test.txt')
print('Файл успешно загружен')
client.download_file(bucket, 'lab9/test.txt', str(downloaded))
print('Файл успешно получен')
if source.read_bytes() != downloaded.read_bytes():
    raise ValueError('Содержимое файлов отличается')
print('Проверка пройдена: содержимое файлов совпадает')
