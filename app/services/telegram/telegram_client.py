from pathlib import Path
import aiofiles
import aiohttp
from services.secrets.secrets import get_secrets
from services.telegram.requests.update_chat import File

class TelegramClient:
   
    def __init__(self) -> None:
        TELEGRAM_BOT_TOKEN = get_secrets().OPENAI_API_KEY
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
        
        file_path = Path('/tmp/') / Path(file["result"]["file_path"])
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.FILE_URL + "/" + file["result"]["file_path"]) as response:
                async with aiofiles.open(file_path.absolute(), 'wb') as f:
                    await f.write(await response.read())