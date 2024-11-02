# AWS-Image-Recognition-Pipeline
This project consists of two main Python applications running on separate AWS EC2 instances. The first 
application (EC2 Instance A) is responsible for detecting cars in images using AWS Rekognition. If a car is 
detected with a confidence level above 90%, the image index is sent to an AWS SQS queue. The second 
application (EC2 Instance B) reads these image indices from the SQS queue, retrieves the corresponding 
images, and uses AWS Rekognition to perform text recognition.

![{34AB7DE5-4723-42A1-971B-817C1DAA1209}](https://github.com/user-attachments/assets/9e4f82c6-48c0-4856-90c8-2964c6d52fca)
