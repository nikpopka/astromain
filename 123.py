import requests

bot_token = ''
chat_id = '910261119'
message_text = 'Привет от вашего Telegram бота!'
send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

payload = {
    'chat_id': chat_id,
    'text': message_text
}

response = requests.post(send_message_url, data=payload)
print(response.json())




