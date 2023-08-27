import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_sns_test')

def handler(event, context):
    try:
        # DynamoDBから最大100件のデータを取得
        response = table.scan(Limit=100)
        
        articles = []
        
        for item in response['Items']:
            article = {
                'userId': item['userId'],
                'name': item['name'],
                'text': item['text'],
                'category': item.get('category', ''),  # categoryがない場合は空文字列を設定
                'reply': item.get('reply', []),  # replyがない場合は空配列を設定
                'likepost': int(item.get('likepost', 0))  # likepostがない場合は0を設定
            }
            # Decimalをintに変換
            if isinstance(article['likepost'], Decimal):
                article['likepost'] = int(article['likepost'])
            
            articles.append(article)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'articles': articles}, default=str)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
