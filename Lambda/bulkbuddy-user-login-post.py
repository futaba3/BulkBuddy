import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_user')

def handler(event, context):
    try:
        # リクエストボディの解析
        body = json.loads(event.get('body', '{}'))
        userId = body.get('userId')
        password = body.get('password')

        # userId または password が存在しない場合のエラーハンドリング
        if not userId or not password:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'userId または password がリクエストに含まれていません。'
                })
            }

        response = table.get_item(
            Key={
                'userId': userId
            }
        )

        if 'Item' in response:
            stored_password = response['Item']['password']
            if stored_password == password:
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'token': 'token'
                    })
                }
            else:
                return {
                    'statusCode': 401,
                    'body': json.dumps({
                        'message': 'userIdまたはpasswordが一致しません。'
                    })
                }
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    'message': 'userIdまたはpasswordが一致しません。'
                })
            }
    except Exception as e:
        # 予期しないエラーのハンドリング
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal Server Error',
                'error': str(e)
            })
        }