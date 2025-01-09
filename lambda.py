import json
import urllib3
import boto3

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:CryptoPriceAlerts" # remeber to change this 
THRESHOLD = 95000  # Set threshold for alerts. Remember to change this also 

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    
    data = json.loads(response.data.decode('utf-8'))
    current_price = data['bitcoin']['usd']
    
    print(f"Current BTC Price: ${current_price}")
    
    if current_price > THRESHOLD:
        send_alert(current_price)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"BTC Price Checked: ${current_price}")
    }

def send_alert(price):
    sns = boto3.client('sns')
    message = f"🚨 Bitcoin Alert: BTC Price is now ${price}, above your threshold of ${THRESHOLD}!"
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Crypto Price Alert"
    )
    print("Alert Sent!")
