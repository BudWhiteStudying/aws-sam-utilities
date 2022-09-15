import boto3
from shared_utils import delete_item, build_success_response, build_failure_response

boto3_client = boto3.client('dynamodb')
table_name = 'Notification_Rule'


# sample invocation:
# http://127.0.0.1:3000/notification_rule?notification-rule-id=SOME_CONFIG


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
        return build_failure_response(repr(e))
    return build_success_response(return_data)
