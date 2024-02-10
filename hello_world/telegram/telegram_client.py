import aiohttp
import os
class TelegramClient:
   
    def __init__(self) -> None:
        TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.API_URL = f"https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage"
    
    
    async def send_message(self, chat_id, text):
        data = {
            'chat_id': chat_id,
            'text': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, data=data) as response:
                return await response.json()
        return None
    
    async def send_photo(self, chat_id, photo_url):
        data = {
            'chat_id': chat_id,
            'photo': photo_url
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, data=data) as response:
                return await response.json()
        return None
    
    async def send_location(self, chat_id, latitude, longitude):
        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, data=data) as response:
                return await response.json()
        return None
    
    async def send_animation(self, chat_id, animation_url):
        data = {
            'chat_id': chat_id,
            'animation': animation_url
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, data=data) as response:
                return await response.json()
        return None
    