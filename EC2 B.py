import boto3

def receive_messages_and_detect_text(bucket_name, queue_url):
    rekognition_client = boto3.client('rekognition')
    sqs_client = boto3.client('sqs')

    empty_responses = 0  # Counter for empty responses

    while True:
        messages = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        if 'Messages' not in messages:
            print("No messages in queue. Waiting...")
            empty_responses += 1
            if empty_responses >= 10:  # Stop after 10 empty responses
                print("No new messages for a while. Stopping.")
                break
            continue

        empty_responses = 0  # Reset counter if a message is found

        message = messages['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        image_key = message['Body']

        response = rekognition_client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': image_key
                }
            }
        )

        print(f"Detected texts for {image_key}:")
        for text_detail in response['TextDetections']:
            print(text_detail['DetectedText'])

        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
if __name__ == '__main__':
    BUCKET_NAME = 's3bucket9542'  # Your S3 bucket name
    QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/774777699946/Sqsqueue9542'  # Your SQS queue URL

    receive_messages_and_detect_text(BUCKET_NAME, QUEUE_URL)
