import json
from appwrite.client import Client
from appwrite.services.databases import Databases

async def main(req):
    # خواندن بدنه درخواست
    body = json.loads(req['body'])
    message = body.get('message', 'بدون پیام')
    user_id = body.get('user_id', 'بدون کاربر')
    
    # تنظیم کلاینت Appwrite
    client = Client()
    client.set_endpoint('https://cloud.appwrite.io/v1')
    client.set_project('6841b8f900220db23a2f')  # آیدی پروژه
    client.set_key('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')  # کلید API

    databases = Databases(client)
    data = {
        'user_id': user_id,
        'message': message,
        'timestamp': str(req['time'])
    }
    # ذخیره سند با ID تصادفی (برای تست، می‌تونی خالی بذاری)
    result = databases.create_document('6841b914003d7bb397e3', '6841b9cd0008179ccbd7', 'test_doc_' + str(req['time']), data)
    
    # برگردوندن پاسخ به‌صورت JSON
    return json.dumps({
        'status': 'success',
        'message': f'پیام ذخیره شد: {message} برای کاربر {user_id}'
    })
