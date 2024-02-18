import aiohttp
import os
import logging

from services.telegram.requests.update_chat import File

class TelegramClient:
   
    def __init__(self) -> None:
        TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        self.FILE_URL = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}"
    
    
    async def send_message(self, chat_id, text):
        url = f"{self.API_URL}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
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
    
    async def get_file(self, file_id) -> File:
        data = {
            'file_id': file_id,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL + "/getFile", data=data) as response:
                return await response.json()
        return None
    
    async def download_file(self, file: File):  
        async with aiohttp.ClientSession() as session:
            async with session.get(self.FILE_URL + "/" + file.file_path) as response:
                return await response.content