import json
import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_user')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def handler(event, context):
    try:
        body = json.loads(event['body'])
        userId = body.get('userId', None)
        calorie = body.get('calorie', None)
        
        if userId is None or calorie is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'userId and calorie are required'})
            }

        response = table.get_item(
            Key={
                'userId': userId
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }

        current_calorie = response['Item'].get('calorie', 0)
        new_calorie = current_calorie + int(calorie)
        timestamp = int(datetime.now().timestamp() * 1000)

        table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression="SET #cal = :new_calorie, #ts = :timestamp",
            ExpressionAttributeValues={
                ':new_calorie': new_calorie,
                ':timestamp': timestamp
            },
            ExpressionAttributeNames={
                '#cal': 'calorie',
                '#ts': 'timestamp'
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'userId': userId,
                'calorie': new_calorie,
                'timestamp': timestamp
            }, default=decimal_default)  # Decimalをintに変換
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }