import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# DecimalをJSONシリアライズ可能な型に変換するヘルパー関数
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# DynamoDBリソースを初期化
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_sns_test')

def handler(event, context):
    try:
        # リクエストからパラメータを取得
        userId = event.get('userId', None)
        category = event.get('category', None)
        likepost_search = event.get('likepost_search', 0)
        
        # クエリまたはスキャンを実行
        if userId:
            query_params = {
                'KeyConditionExpression': Key('userId').eq(userId)
            }
            if category:
                query_params['FilterExpression'] = Key('category').eq(category)
            response = table.query(**query_params)
            items = response['Items']
        else:
            scan_params = {}
            if category:
                scan_params['FilterExpression'] = Key('category').eq(category)
            response = table.scan(**scan_params)
            items = response['Items']
        
        # 結果をソート
        if likepost_search == 1:
            # いいねが多い順にソート
            items = sorted(items, key=lambda x: x['likepost'], reverse=True)
        else:
            # timestampで新しい順にソート
            items = sorted(items, key=lambda x: x['timestamp'], reverse=True)
        
        # レスポンスを準備
        articles = []
        for item in items:
            article = {
                'userId': item['userId'],
                'name': item['name'],
                'category': item['category'],
                'reply': item['reply'],
                'likepost': item['likepost']
            }
            articles.append(article)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'articles': articles
            }, default=decimal_default)  # Decimalをfloatに変換
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
