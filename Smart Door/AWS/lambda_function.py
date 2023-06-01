import json
import boto3
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# DynamoDB table name
table_name = 'sensors_data'

def lambda_handler(event, context):
    # Extract sensor values from the event message
    distance = event.get('distance')
    movement = event.get('pir-sensor')

    # Validate and convert the values
    try:
        distance = float(distance)
        movement = int(movement)
    except (ValueError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid sensor values')
        }

    # Generate a timestamp
    timestamp = datetime.now().isoformat()

    # Prepare the item to be inserted into DynamoDB
    item = {
        'ID': {'S': timestamp},  # Use timestamp as the ID for each row
        'sonar': {'N': str(distance)},
        'pir': {'N': str(movement)}
    }

    # Insert the item into DynamoDB
    try:
        response = dynamodb.put_item(TableName=table_name, Item=item)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error inserting data into DynamoDB: {str(e)}')
        }

    # Return a success response
    return {
        'statusCode': 200,
        'body': json.dumps('Data inserted into DynamoDB successfully')
    }
