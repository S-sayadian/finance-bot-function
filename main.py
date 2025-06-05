import os
import json
import requests
from appwrite.client import Client
from appwrite.services.databases import Databases
from datetime import datetime

def parse_with_llama(message, api_key, api_url):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""تو یک دستیار حسابداری هستی. پیام زیر را تحلیل کن و اطلاعات تراکنش را به‌صورت JSON استخراج کن. فقط اطلاعات زیر را برگردان:
{{
    "type": "expense|income|loan|debt",
    "amount": <مبلغ به‌صورت عدد>,
    "counterparty": "<نام طرف حساب یا خالی>",
    "description": "<متن کامل پیام>"
}}
مثال: "۲۰۰۰ تومان به محمد دادم" → {{"type": "loan", "amount": 2000, "counterparty": "محمد", "description": "۲۰۰۰ تومان به محمد دادم"}}
پیام: {message}
"""
    payload = {
        "model": "meta-llama/Llama-3-8b-hf",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        result = json.loads(response.json()['choices'][0]['message']['content'])
        return result
    except Exception as e:
        return {"error": f"خطا در پردازش با LLaMA: {str(e)}"}

def main(req, res):
    try:
        payload = json.loads(req['body'])
        message = payload.get('message')
        user_id = payload.get('user_id')

        # پردازش پیام با LLaMA
        llama_result = parse_with_llama(message, os.environ['LLAMA_API_KEY'], os.environ['LLAMA_API_URL'])
        if 'error' in llama_result:
            return res.json({'status': 'error', 'message': llama_result['error']}, 500)

        # افزودن اطلاعات اضافی
        data = llama_result
        data['user_id'] = str(user_id)
        data['timestamp'] = datetime.utcnow().isoformat()

        # ذخیره در Appwrite
        client = Client()
        client.set_endpoint('https://cloud.appwrite.io/v1') \
              .set_project(os.environ['APPWRITE_PROJECT_ID'])
        db = Databases(client)
        db.create_document(
            database_id=os.environ['APPWRITE_DATABASE_ID'],
            collection_id=os.environ['APPWRITE_COLLECTION_ID'],
            document_id='unique()',
            data=data
        )

        # پاسخ به کاربر
        response_message = f"""
✅ تراکنش ثبت شد:
💰 مبلغ: {data['amount']} تومان
📂 نوع: {data['type']}
📝 توضیح: {data['description']}
{f"👤 طرف حساب: {data['counterparty']}" if data['counterparty'] else ""}
🕒 زمان: {data['timestamp']}
"""
        return res.json({'status': 'success', 'message': response_message})

    except Exception as e:
        return res.json({'status': 'error', 'message': f'خطا: {str(e)}'}, 500)