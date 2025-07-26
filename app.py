import discord
from discord.ext import commands
from dotenv import load_dotenv # تحميل المتغيرات من ملف .env
import os
import asyncio
import subprocess
import sys
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests



load_dotenv() # تحميل المتغيرات من ملف .env

# تعريف token البوت
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# تشغيل البوت
async def start_bot():
    if not TOKEN:
        print("🔴 Error: DISCORD_TOKEN not found in .env file.")
        return
    else:
        print("🟢 DISCORD_TOKEN found in .env file.")
    print("🔵 Starting the bot...")

    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"🔴 Error starting the bot: {e}")

# إعداد البوت
print("🔧 Initializing the bot...")
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('🏓 Pong!')


# قرات commands من الفولدر commands
def scan_commands():
    print("📂 Scanning for commands...")
    if not os.path.exists('./commands'):
        print("🔴 'commands' directory not found. Please create it and add command files.")
    else:
        print("🟢 'commands' directory found.")

async def load_commands():
    print("🔍 Loading commands...")
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'🟢 Loaded Cog: {filename}')
            except Exception as e:
                print(f'🔴 Failed to load Cog "{filename}": {e}')
        else:
            print(f'🔴 Skipped non-Python file: {filename}')


async def load_events():
    print("🔍 Loading events from 'module' folder...")
    events_path = './module'
    if not os.path.exists(events_path):
        print("🔴 'module' directory not found. Please create it and add event files.")
        return
    for filename in os.listdir(events_path):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'module.{filename[:-3]}')
                print(f'🟢 Loaded Event: {filename}')
            except Exception as e:
                print(f'🔴 Failed to load Event "{filename}": {e}')
        else:
            print(f'🔴 Skipped non-Python file: {filename}')

# بدء البوت
async def main():
    scan_commands()
    await load_commands()
    await load_events()
    print("✅ All Cogs loaded successfully.")
    print("🚀 Starting the bot...")
    await start_bot()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Bot stopped by user. Goodbye!")
        sys.exit(0)