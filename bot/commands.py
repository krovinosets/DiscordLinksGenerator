import asyncio

from config import COMMAND_HELP_TEXT
from database.manager import DataBase
import math
import discord


class CommandList(object):

    async def create(self, amount: int, channel: any, expire: int) -> str:
        """
        Creating unique links to discord server and
        adding to Data Base with links

        :param expire:
        :param channel:
        :param amount:
        :return:
        """
        if channel is None:
            return f'Канал для создания ссылок не найден. Проверьте корректность введного id канала.'

        if amount <= 0:
            return f'Нельзя создать меньше 1(одной) ссылки.'

        if expire <= 600 and expire != 0:
            return f'Нельзя создать ссылку, которая истекает менее, чем через 10 минут.'

        print("===================")
        print(f'Запрос: Создать {amount} приглашений.')

        cycles = 1
        estimated = amount
        if amount > 15:
            cycles = amount / (5 * (len(str(amount)) - 1))
        per_cycle = estimated // math.floor(cycles)
        cycles = math.ceil(cycles)
        print(f'Количество циклов на запрос: {cycles}')

        db = DataBase()
        db.create_connection()
        for i in range(1, cycles + 1):
            passed = 0
            for passed in range(1, per_cycle + 1 if estimated > per_cycle else estimated + 1):
                link = await channel.create_invite(max_age=expire, max_uses=1)
                db.insert(link)
            if i != cycles:
                await asyncio.sleep(3)
            print(f'Создано за цикл {passed} приглашений.')
            estimated -= passed
            print(f'Осталось создать {estimated} ({estimated * 100 /amount}%)')
        print("===================")

        return f"Все {amount} приглашений созданы. Остаток {estimated}."

    async def help(self) -> str:
        """
        Getting message from ./config.py

        :return: bot help message as str
        """
        return COMMAND_HELP_TEXT
