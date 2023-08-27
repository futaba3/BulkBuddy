import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_user')

def handler(event, context):
    try:
        body = json.loads(event['body'])
        userId = body.get('userId', None)
        password = body.get('password', None)
        
        # userIdとpasswordは必須
        if userId is None or password is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'userId and password are required'})
            }

        # DynamoDBから指定されたuserIdとpasswordでユーザーを検索
        response = table.get_item(
            Key={
                'userId': userId
            }
        )
        
        if 'Item' not in response or response['Item'].get('password') != password:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found or password incorrect'})
            }

        # ユーザー情報の削除
        table.delete_item(
            Key={
                'userId': userId
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }