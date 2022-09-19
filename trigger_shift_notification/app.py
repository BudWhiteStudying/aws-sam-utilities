import json
import boto3
from datetime import datetime, timedelta
import traceback
from shared_utils import build_success_response, build_failure_response

lambda_client = boto3.client('lambda')


# sample invocation:
# http://127.0.0.1:3000/notification_rule?notification-rule-id=SOME_CONFIG

def get_shift_by_date(client, reference_date):
    return_data = client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:725885754378:function:shift-manager-cf-stack-GetNamedShiftFunction-aTb2PqG8t2hZ',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "queryStringParameters": {
                "reference-date": reference_date
            }})
    )
    shift = None
    if 'Payload' in return_data:
        payload = json.load(return_data['Payload'])
        print('Lambda returned {data}'.format(data=payload))
        if 'body' in payload and 'data' in payload['body']:
            shift = payload['body']['data']
    return shift


def lambda_handler(event, context):
    try:
        current_shift_date = datetime.today()
        next_shift_date = current_shift_date+timedelta(days=1)

        current_shift = get_shift_by_date(lambda_client, current_shift_date.strftime('%Y-%m-%d'))
        next_shift = get_shift_by_date(lambda_client, next_shift_date.strftime('%Y-%m-%d'))

        if current_shift['operator_id'] == next_shift['operator_id']:
            print('No change of shift, no need to send an email')
        else:
            print('Change of shift detected, will trigger an email with named {name1} and {name2}'.format(name1=current_shift['operator_name'],name2=next_shift['operator_name']))
    except Exception as e:
        tb = traceback.format_exc()
        print('we failed: ' + repr(tb))
        return build_failure_response(repr(tb))
    return build_success_response({'current_shift': current_shift, 'next_shift': next_shift})
