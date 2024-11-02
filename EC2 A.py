import boto3

def detect_cars_and_send_to_sqs(bucket_name, image_keys, queue_url):
    rekognition_client = boto3.client('rekognition')
    sqs_client = boto3.client('sqs')

    for image_key in image_keys:
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': image_key
                }
            },
            MaxLabels=10,
            MinConfidence=75
        )

        # Check if 'Car' is detected and confidence > 90%
        for label in response['Labels']:
            if label['Name'] == 'Car' and label['Confidence'] > 90:
                print(f"Car detected in {image_key} with confidence {label['Confidence']}")
                # Send the image key to SQS
                sqs_client.send_message(
                    QueueUrl=queue_url,
                    MessageBody=image_key
                )
                break

if __name__ == '__main__':
    BUCKET_NAME = 's3bucket9542'
    IMAGE_KEYS = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg']
    QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/774777699946/Sqsqueue9542'  # Replace with your SQS queue URL

    detect_cars_and_send_to_sqs(BUCKET_NAME, IMAGE_KEYS, QUEUE_URL)
