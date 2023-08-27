import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_sns_test')

def handler(event, context):
    try:
        body = json.loads(event['body'])
        
        userId = body.get('userId', None)
        timestamp = body.get('timestamp', None)
        
        if userId is None or timestamp is None:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'userId and timestamp are required'})
            }
        
        # 先に該当するアイテムを検索
        response = table.query(
            KeyConditionExpression=Key('userId').eq(userId),
            FilterExpression=Key('timestamp').eq(int(timestamp))
        )
        
        if 'Items' in response and len(response['Items']) > 0:
            likepost = response['Items'][0]['likepost']
            
            # 該当するアイテムを削除
            table.delete_item(
                Key={
                    'userId': userId,
                    'likepost': likepost
                }
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Successfully deleted'})
            }
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Item not found'})
            }
        
    except Exception as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': str(e)})
        }
