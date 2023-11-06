import asyncio

import discord
from bot.commands import CommandList
from config import GUILD_ID

ID = discord.Object(id=GUILD_ID)


class Bot(discord.Client):

    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)

        """
        Creating interaction commands aliases
        """
        self.decorator = discord.app_commands
        self.tree = self.decorator.CommandTree(self)
        self.commands = CommandList()

        """
        Definition of interaction commands
        """
        self.main_cmd = self.decorator.describe(amount="Создание ссылок-приглашений") \
            (
                self.decorator.rename(amount="количество")
                (
                    self.tree.command(name="create", description="Создать ссылки", guild=ID)
                    (
                        self.create
                    )
                )
            )
        self.help = self.decorator.describe() \
            (
                self.tree.command(name="help", description="Получить описание команд", guild=ID)
                (
                    self.help
                )
            )

    async def help(self, interaction: discord.Interaction):
        """
        Get help message of bot commands

        :param interaction: links interaction ability of command
        :return: bot help message
        """
        result = await asyncio.create_task(self.commands.help())
        await interaction.response.send_message(f'{result}')

    async def create(self, interaction: discord.Interaction, amount: str, channel: str, time: str):
        """
        Create [AMOUNT] unique links to discord server

        :param time:
        :param channel:
        :param interaction: links interaction ability of command
        :param amount: amount of creating links
        :return: bot creating result message
        """

        channel = discord.utils.get(self.guilds[0].channels, id=int(channel))

        await interaction.response.defer()
        result = await asyncio.create_task(self.commands.create(int(amount), channel, int(time)))
        await interaction.followup.send(f'{result}')


    async def setup_hook(self):
        self.tree.copy_global_to(guild=ID)
        await self.tree.sync(guild=ID)

    async def on_ready(self):
        print(f'Бот {self.user} запущен')
