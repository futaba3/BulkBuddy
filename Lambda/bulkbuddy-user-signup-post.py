import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('team1_user')

def calculate_age(birth_year, birth_month, birth_day):
    today = datetime.today()
    age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
    return age

def handler(event, context):
    try:
        body = json.loads(event['body'])
        userId = body.get('userId')
        name = body.get('name')
        password = body.get('password')
        height = body.get('height')
        weight = body.get('weight')
        birth_year = body.get('birth_year')
        birth_month = body.get('birth_month')
        birth_day = body.get('birth_day')
        gender = body.get('gender')
        targetWeight = body.get('targetWeight', None)
        targetDate = body.get('targetDate', None)

        # 必須フィールドの確認
        if not all([userId, name, password, height, weight, birth_year, birth_month, birth_day, gender]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'All required fields must be provided'})
            }

        # 年齢の計算
        age = calculate_age(birth_year, birth_month, birth_day)

        # DynamoDBに保存
        table.put_item(
            Item={
                'userId': userId,
                'name': name,
                'password': password,
                'height': height,
                'weight': weight,
                'birth_year': birth_year,
                'birth_month': birth_month,
                'birth_day': birth_day,
                'age': age,
                'gender': gender,
                'calorie': 0,
                'targetWeight': targetWeight,
                'targetDate': targetDate
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'userId': userId,
                'name': name,
                'height': height,
                'weight': weight,
                'age': age,
                'calorie': 0,
                'targetWeight': targetWeight,
                'targetDate': targetDate,
                'token': 'mtiToken'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }