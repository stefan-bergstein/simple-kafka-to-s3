#! /usr/bin/env python3

import time
import os
from kafka import KafkaConsumer
import boto3
from botocore.exceptions import ClientError


def main():

    #
    # Get some settings from the env
    #
    
    s3_bucket = os.getenv('S3_BUCKET', 'my-bucket')
    s3_path = os.getenv('S3_PATH', 'data')
    s3_access_key = os.environ['ACCESS_KEY_ID']
    s3_secret_key = os.environ['SECRET_ACCESS_KEY']
    s3_endpoint = os.environ['S3_ENDPOINT']
    filename_prefix = os.getenv('FILENAME_PREFIX','samples')

    kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS','localhost:9092')
    kafka_topic = os.getenv('KAFKA_TOPIC','iot-sensor-sw-vibration')

    print('KAFKA_BOOTSTRAP_SERVERS:',kafka_bootstrap_servers)
    print('KAFKA_TOPIC:',kafka_topic)
    
    
    #
    # Connect to Kafka
    #
    
    for t in range(5):
        try:
            consumer = KafkaConsumer(
                kafka_topic,
                bootstrap_servers=[kafka_bootstrap_servers],
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                group_id='s3-group')
            break
        except:
            print("KafkaConsumer error. Retry ....", t)
            time.sleep(5)
        
    #
    # Get messages from kafka a save to a local file
    #
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file_name = filename_prefix + "-" + kafka_topic + "-"  + timestr + ".csv"
    
    file = open(file_name,"w+") 
    for x in range(100):
        msgs=consumer.poll(timeout_ms=5000,max_records=500)
        num_records=0
        for topicpartition in list(msgs.keys()):
            records = msgs[topicpartition]
            print("Save msgs to file. #:", len(records))
            for m in records:
                file.write(m.topic + "," + m.value.decode('utf-8')  + "\n") 
            num_records=+len(records)
        print("num_records:", num_records)
        if num_records < 10:
            break
    file.close()
    
    
    #
    # Upload to S3
    #
    
    s3 = boto3.client(service_name='s3', aws_access_key_id = s3_access_key,
                      aws_secret_access_key = s3_secret_key, 
                      endpoint_url=s3_endpoint, use_ssl=True, verify=False)

    s3_file = s3_path + "/" + file_name

    print("Upload to S3:",s3_file)
    
    for t in range(5):
        try:
            s3.upload_file(file_name, s3_bucket, s3_file)
            break
        except ClientError as e:
            print(e)
            print("s3.upload_file error. Retry ....", t)
            time.sleep(5)
            
    consumer.commit()
    consumer.close()

if __name__ == '__main__':
    main()



