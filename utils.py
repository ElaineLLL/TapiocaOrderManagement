import json
import boto3

def Changedata(name,value):
    with open("config.json",'r',encoding='utf-8') as load_f:
        d = json.load(load_f)
    d[name] = value
    with open("config.json",'w',encoding='utf-8') as f:
        json.dump(d, f,ensure_ascii=False)

def Readdata(name):
    with open("config.json",'r',encoding='utf-8') as load_f:
        d = json.load(load_f)
    return d[name]


def publish_to_sns(topic_arn, message, subject=None):
    """
    Publishes a message to an AWS SNS topic.

    Parameters:
    - topic_arn (str): The Amazon Resource Name (ARN) of the SNS topic.
    - message (str): The message you want to send.
    - subject (str, optional): The subject of the message.

    Returns:
    - dict: The response from the SNS service.
    """
    sns_client = boto3.client('sns', region_name='us-east-1', aws_access_key_id="AKIAXLCBMEJBTX6PQSWQ",
         aws_secret_access_key= "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")

    # Construct the parameters for the publish API call
    params = {
        'TopicArn': topic_arn,
        'Message': message,
    }

    # Add subject if provided
    if subject:
        params['Subject'] = subject

    # Publish the message to the specified SNS topic
    response = sns_client.publish(**params)

    return response

# Example Usage:
if __name__ == '__':
    topic_arn = 'arn:aws:sns:us-east-1:504795767363:sent'
    message = 'Hello, this is a test message!'
    subject = 'Test Subject'

    response = publish_to_sns(topic_arn, message, subject)
    print(response)
