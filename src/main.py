import discord

from client import ScoutClient
from config import Config


def main():
    intents = discord.Intents.default()
    intents.message_content = True

    client = ScoutClient(intents=intents)
    client.run(Config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
