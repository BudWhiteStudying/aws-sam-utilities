import json
import boto3

boto3_client = boto3.client('dynamodb')
table_name = 'Notification_Rule'


# sample invocation:
# http://127.0.0.1:3000/notification_rule?notification-rule-id=SOME_CONFIG

def delete_item(dynamodb_client, table_name, key):
    return_data = dynamodb_client.delete_item(
        TableName=table_name,
        Key=key
    )
    return return_data


def build_success_response(table_name, success_data):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Deleted item on table {table}: {data}".format(table=table_name, data=success_data)
        })
    }


def build_failure_response(table_name, failure_data):
    return {
        "statusCode": 500,
        "body": json.dumps({
            "message": "Problems deleting item on table {table}: {error}".format(
                table=table_name, error=failure_data)
        })
    }


def lambda_handler(event, context):
    try:
        notification_rule_id = event['queryStringParameters']['id']

        if notification_rule_id is None:
            print('Missing parameter id')
            raise Exception('Missing parameter id')

        return_data = delete_item(
            boto3_client,
            table_name,
            {'id': {'S': notification_rule_id}}
        )
    except Exception as e:
        print('we failed: ' + repr(e))
        return build_failure_response(table_name, repr(e))
    return build_success_response(table_name, return_data)
