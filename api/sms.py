import messagebird
from config.config import Config


def send_verification_sms(user_phone, verification_code):
    client = messagebird.Client(Config.SMS_API_KEY)
    sms_message = str(verification_code) +  ' is your pharma verification code'
    message = client.message_create(
        'Pharma',
        user_phone,
        sms_message,
    )

    return True


