import json

async def main(req, res):
    body = json.loads(req['body'])
    message = body.get('message', 'بدون پیام')
    user_id = body.get('user_id', 'بدون کاربر')
    
    # ذخیره ساده توی دیتابیس (برای تست)
    from appwrite.client import Client
    from appwrite.services.databases import Databases

    client = Client()
    client.set_endpoint('https://cloud.appwrite.io/v1')  # URL Appwrite
    client.set_project('6841b8f900220db23a2f')  # جای این آیدی پروژه‌ت رو بذار
    client.set_key('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')  # جای این کلید API پروژه‌ت رو بذار

    databases = Databases(client)
    data = {
        'user_id': user_id,
        'message': message,
        'timestamp': str(req['time'])
    }
    result = databases.create_document('6841b914003d7bb397e3', '6841b9cd0008179ccbd7', '[DOCUMENT_ID]', data)
    
    # برگردوندن خروجی
    return res.json({
        'status': 'success',
        'message': f'پیام ذخیره شد: {message} برای کاربر {user_id}'
    })
