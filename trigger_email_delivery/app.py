import boto3
import traceback
import json
import html
from shared_utils import build_success_response, build_failure_response

ses_client = boto3.client('ses')
lambda_client = boto3.client('lambda')


# sample invocation:
# http://127.0.0.1:3000/notification_rule?notification-rule-id=SOME_CONFIG


def get_notification_rule(rule_id):
    return_data = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:725885754378:function:shift-manager-cf-stack-GetNotificationRuleFunction-UFE9IkgsxQsH',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "queryStringParameters": {
                "id": rule_id
            }})
    )
    notification_rule = None
    if 'Payload' in return_data:
        payload = json.load(return_data['Payload'])
        print('Lambda returned {data}'.format(data=payload))
        if 'body' in payload and\
                'data' in payload['body'] and\
                'value' in payload['body']['data'] and\
                'S' in payload['body']['data']['value']:
            notification_rule = payload['body']['data']['value']['S']
    return notification_rule


def send_email(client, source_address, recipients_to, recipients_cc, subject, html_body, text_body):
    return_data = client.send_email(
        Destination={
            "ToAddresses": [
                recipients_to
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": html_body,
                },
                "Text": {
                    "Charset": "UTF-8",
                    "Data": text_body,
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": subject,
            },
        },
        Source=source_address,
        ReturnPath=source_address
    )
    print('SES returned {data}'.format(data=return_data))
    return return_data


def lambda_handler(event, context):
    try:

        finishing_operator_name = event['queryStringParameters']['finishing-operator-name'] \
            if 'finishing-operator-name' in event['queryStringParameters'] \
            else None
        starting_operator_name = event['queryStringParameters']['starting-operator-name'] \
            if 'starting-operator-name' in event['queryStringParameters'] \
            else None

        if finishing_operator_name is None or starting_operator_name is None:
            raise Exception('finishing-operator-name and starting-operator-name params are mandatory')

        email_subject = get_notification_rule('NOTIFICATION_EMAIL_SUBJECT')
        email_body_html_template = get_notification_rule('NOTIFICATION_EMAIL_BODY_HTML_TEMPLATE')
        email_body_text_template = get_notification_rule('NOTIFICATION_EMAIL_BODY_TEXT_TEMPLATE')
        email_recipients_to = get_notification_rule('NOTIFICATION_EMAIL_RECIPIENTS_TO')
        email_source_address = get_notification_rule('NOTIFICATION_EMAIL_SOURCE_ADDRESS')

        delivery_data = send_email(
            ses_client,
            email_source_address,
            email_recipients_to,
            None,
            email_subject,
            email_body_html_template.format(
                finishing_operator_name=finishing_operator_name,
                starting_operator_name=starting_operator_name),
            email_body_text_template.format(
                finishing_operator_name=finishing_operator_name,
                starting_operator_name=starting_operator_name))

    except Exception as e:
        tb = traceback.format_exc()
        print('we failed: ' + repr(tb))
        return build_failure_response(repr(tb))
    return build_success_response({'delivery_data': delivery_data})
