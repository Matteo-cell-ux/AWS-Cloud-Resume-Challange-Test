import json
import boto3

# Inizializza il client DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloudresume-test')

def handler(event, context):
    # 1. Recupera il metodo HTTP in modo compatibile con Function URL
    method = event.get('requestContext', {}).get('http', {}).get('method')
    
    # 2. Gestione richiesta OPTIONS (Preflight per CORS)
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }

    # 3. Incremento atomico del contatore nel database
    try:
        response = table.update_item(
            Key={'id': '0'},
            UpdateExpression='ADD #v :inc',
            ExpressionAttributeNames={'#v': 'views'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues="UPDATED_NEW"
        )

        views = int(response['Attributes']['views'])

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'views': views})
        }
        
    except Exception as e:
        # In caso di errore, restituiamo un errore leggibile
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }