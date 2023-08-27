import json
import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_user')

def calculate_age(birth_year, birth_month, birth_day):
    today = datetime.today()
    age = today.year - int(birth_year) - ((today.month, today.day) < (int(birth_month), int(birth_day)))
    return age

def handler(event, context):
    try:
        # クエリパラメータから userId を取得
        userId = event['queryStringParameters'].get('userId', None) if event.get('queryStringParameters') else None

        # クエリパラメータがない場合、リクエストボディから userId を取得
        if userId is None:
            body = json.loads(event.get('body', '{}'))
            userId = body.get('userId', None)
        
        if userId is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'userId is required'})
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
        
        item = response['Item']
        
        age = calculate_age(int(item['birth_year']), int(item['birth_month']), int(item['birth_day']))
        
        user_data = {
            'userId': item['userId'],
            'name': item['name'],
            'height': int(item.get('height', 0)) if item.get('height') is not None else None,
            'weight': int(item.get('weight', 0)) if item.get('weight') is not None else None,
            'age': age,
            'calorie': int(item.get('calorie', 0)) if item.get('calorie') is not None else None,
            'targetWeight': int(item.get('targetWeight', 0)) if item.get('targetWeight') is not None else None,
            'targetDate': int(item.get('targetDate', 0)) if item.get('targetDate') is not None else None,
            'gender': int(item.get('gender', 0)) if item.get('gender') is not None else None
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(user_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }