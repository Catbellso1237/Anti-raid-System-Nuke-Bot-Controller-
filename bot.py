"""
Entry point của bot Anti-Nuke.
Chạy: python bot.py
"""
import asyncio
import logging

import aiohttp
import discord
from discord.ext import commands

import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("bot")

INTENTS = discord.Intents.default()
INTENTS.members = True  # cần để lấy member object khi tước quyền/ban
INTENTS.guilds = True
INTENTS.moderation = True  # audit log / ban events


class AntiNukeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=INTENTS)
        self.http_session: aiohttp.ClientSession | None = None

    async def setup_hook(self):
        self.http_session = aiohttp.ClientSession()
        await self.load_extension("cogs.anti_nuke")
        logger.info("Đã tải cog anti_nuke")

    async def close(self):
        if self.http_session:
            await self.http_session.close()
        await super().close()

    async def on_ready(self):
        app_info = await self.application_info()
        self.owner_id = app_info.owner.id
        logger.info(f"Đăng nhập thành công: {self.user} (ID: {self.user.id})")
        logger.info(f"Owner: {app_info.owner} ({app_info.owner.id})")
        logger.info(f"Đang bảo vệ {len(self.guilds)} server.")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="hành vi nuke server"
            )
        )


async def main():
    bot = AntiNukeBot()
    async with bot:
        await bot.start(config.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
