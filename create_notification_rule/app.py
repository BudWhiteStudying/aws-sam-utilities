import json
import boto3

boto3_client = boto3.client('dynamodb')
table_name = 'Notification_Rule'


# sample invocation:
# http://127.0.0.1:3000/notification_rule?notification-rule-value=SOME_VALUE&notification-rule-id=SOME_CONFIG

def put_item(dynamodb_client, table_name, item):
    return_data = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )
    return return_data


def build_success_response(table_name, success_data):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Created a new item on table {table}: {data}".format(table=table_name, data=success_data)
        })
    }


def build_failure_response(table_name, failure_data):
    return {
        "statusCode": 500,
        "body": json.dumps({
            "message": "Problems creating a new item on table {table}: {error}".format(
                table=table_name, error=failure_data)
        })
    }


def lambda_handler(event, context):
    try:
        notification_rule_id = event['queryStringParameters']['notification-rule-id']
        notification_rule_value = event['queryStringParameters']['notification-rule-value']
        print(
            'notification_rule_id is {notification_rule_id}, notification_rule_value is {notification_rule_value}'.format(
                notification_rule_id=notification_rule_id, notification_rule_value=notification_rule_value))

        if notification_rule_id is None or notification_rule_value is None:
            print('Missing notification_rule_id and/or notification_rule_value')
            raise Exception('Missing notification_rule_id and/or notification_rule_value')

        return_data = put_item(
            boto3_client,
            table_name,
            {
                'id': {'S': notification_rule_id},
                'value': {'S': notification_rule_value}
            }
        )
    except Exception as e:
        print('we failed: ' + repr(e))
        return build_failure_response(table_name, repr(e))
    return build_success_response(table_name, return_data)
