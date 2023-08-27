import json
import boto3
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
        
        if userId is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'userId is required'})
            }

        # password のチェックを削除
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

        update_data = {key: body[key] for key in body if key != 'userId'}
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in update_data)
        expression_values = {f":{k}": v for k, v in update_data.items()}
        expression_names = {f"#{k}": k for k in update_data}

        table.update_item(
            Key={
                'userId': userId
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names
        )

        updated_response = table.get_item(
            Key={
                'userId': userId
            }
        )
        updated_item = updated_response['Item']

        user_data = {
            'userId': updated_item['userId'],
            'name': updated_item.get('name', None),
            'height': updated_item.get('height', None),
            'weight': updated_item.get('weight', None),
            'birth_year': updated_item.get('birth_year', None),
            'birth_month': updated_item.get('birth_month', None),
            'birth_day': updated_item.get('birth_day', None),
            'targetWeight': updated_item.get('targetWeight', None),
            'targetDate': updated_item.get('targetDate', None),
            'gender': updated_item.get('gender', None)
        }

        return {
            'statusCode': 200,
            'body': json.dumps(user_data, default=decimal_default)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
