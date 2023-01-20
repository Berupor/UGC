import os
import telegram
import asyncio


async def send_telegram_message(api_token, chat_id, message):
    bot = telegram.Bot(token=api_token)
    await bot.send_message(chat_id=chat_id, text=message)


api_token = os.environ["API_TOKEN"]
chat_id = os.environ["CHAT_ID"]
message = "CI tests passed successfully!"

asyncio.run(send_telegram_message(api_token, chat_id, message))
