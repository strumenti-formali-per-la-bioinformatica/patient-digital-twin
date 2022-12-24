import boto3

def download():
    s3 = boto3.client('s3', region_name='eu-central-1')
    bucket = 'digital-patient-twin-bucket'
    for obj in s3.list_objects(Bucket=bucket)['Contents']:
        if obj['Key'].count('.') == 1:
            print(obj['Key'])
            s3.download_file(bucket, obj['Key'], obj['Key'].rsplit('/', 1)[1])