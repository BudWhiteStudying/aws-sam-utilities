import boto3
from shared_utils import put_item, build_success_response, build_failure_response

boto3_client = boto3.client('dynamodb')
table_name = 'Notification_Rule'


# sample invocation:
# http://127.0.0.1:3000/notification_rule?value=SOME_VALUE&id=SOME_CONFIG


def lambda_handler(event, context):
    try:
        notification_rule_id = event['queryStringParameters']['id']
        notification_rule_value = event['queryStringParameters']['value']
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
        return build_failure_response(repr(e))
    return build_success_response(return_data)
