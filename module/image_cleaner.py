import discord
from discord.ext import commands
import json
import os

class ImageCleaner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
        # تحقق إذا كانت الرسالة تحتوي على صورة
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    try:
                        # تنزيل الصورة
                        img_bytes = await attachment.read()
                        from rembg import remove
                        from io import BytesIO
                        result_img = remove(img_bytes)
                        result_io = BytesIO(result_img)
                        result_io.seek(0)
                        await message.channel.send(file=discord.File(result_io, filename='no_bg.png'))
                    except Exception as e:
                        await message.channel.send(f"حدث خطأ أثناء معالجة الصورة: {e}")

async def setup(bot):
    await bot.add_cog(ImageCleaner(bot))
