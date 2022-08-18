from twilio.rest import Client
from datetime import datetime

account_sid = 'ACae3c6bf7c3b06eb335b1f06a5e3c4d74'
auth_token = 'cf32a22a4fadddabf6506d3f5361913d'
client = Client(account_sid, auth_token)

#numbers = ['+19806225619', '+19806216434']
numbers = ['+19806225619', '+19806216434', '+14845056035']

def in_(fTeam, i_fmLine):

    for number in numbers:

        datetime_str = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        body = f'Cash-In $35.00 on {fTeam} {i_fmLine} Moneyline'

        client.messages.create(
            body = body,
            from_ = '+13252465980',
            to = number
        )

def out(fTeam, i_fmLine, o_fmLine):

    for number in numbers:

        datetime_str = str(datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        body = f'Cash-Out of {fTeam} {i_fmLine} Moneyline @{o_fmLine}'

        client.messages.create(
            body = body,
            from_ = '+13252465980',
            to = number
        )
