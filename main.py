import discord
from config import BOT_TOKEN
from bot.discordBot import Bot


def start():
    client = Bot(intents=discord.Intents().all())
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    start()
