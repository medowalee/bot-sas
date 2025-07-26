

import discord
from discord.ext import commands
import json
import os
import requests
from io import BytesIO

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # تحميل معرف الروم من data.json
        self.target_channel_id = None
        self._load_channel_id()

    def _load_channel_id(self):
        data_path = os.path.join(os.path.dirname(__file__), '../data.json')
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    self.target_channel_id = data.get('channel_id')
                except Exception as e:
                    print(f"خطأ في قراءة data.json: {e}")
        else:
            print("data.json غير موجود")

    @commands.Cog.listener()
    async def on_message(self, message):
        # تجاهل رسائل البوت نفسه
        if message.author == self.bot.user:
            return

        # تحقق من الروم المستهدف
        if not self.target_channel_id or str(message.channel.id) != str(self.target_channel_id):
            return

        # تحقق من صيغة الرسالة
        if message.content.startswith("انشي سورة "):
            prompt = message.content[len("انشي سورة "):].strip()
            if not prompt:
                await message.channel.send("يرجى كتابة محتوى الصورة بعد الأمر.")
                return
            # استخدام DeepAI API لإنشاء صورة
            DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')
            if not DEEPAI_API_KEY:
                await message.channel.send("يرجى إضافة مفتاح DeepAI في ملف .env باسم DEEPAI_API_KEY")
                return
            try:
                response = requests.post(
                    "https://api.deepai.org/api/text2img",
                    data={ 'text': prompt },
                    headers={ 'api-key': DEEPAI_API_KEY }
                )
                result = response.json()
                image_url = result.get('output_url')
                if image_url:
                    try:
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            img_bytes = BytesIO(img_response.content)
                            await message.channel.send(file=discord.File(img_bytes, filename='ai_image.png'))
                        else:
                            await message.channel.send("تعذر تحميل الصورة من DeepAI.")
                    except Exception as e:
                        await message.channel.send(f"حدث خطأ أثناء تحميل الصورة: {e}")
                else:
                    await message.channel.send("تعذر إنشاء الصورة. حاول مرة أخرى أو تحقق من النص.")
            except Exception as e:
                await message.channel.send(f"حدث خطأ أثناء الاتصال بـ DeepAI: {e}")
        else:
            await message.channel.send("اكتب كا التالي :\nانشي سورة (المحتو انشا السوة)")

async def setup(bot):
    await bot.add_cog(OnMessage(bot))