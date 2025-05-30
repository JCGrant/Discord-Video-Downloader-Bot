import re
import os

import discord
import yt_dlp


url_regex = r"(https?://[^\s]+)"


class ScoutClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

    async def on_message(self, message):
        if message.author == self.user:
            return
        urls = re.findall(url_regex, message.content)
        for url in urls:
            random_name = os.urandom(8).hex()
            # Try to download the video
            try:
                ydl_opts = {
                    "outtmpl": os.path.join("downloads", random_name + ".%(ext)s"),
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                continue

            # Inform the user that the video is being processed
            await message.add_reaction("👍")

            video_title = info["title"]
            extension = info["ext"]
            file_path = os.path.join("downloads", f"{random_name}.{extension}")

            # Try to upload the video
            try:
                print(f"Uploading {video_title} @ {file_path}")
                await message.channel.send(file=discord.File(file_path))
            except Exception as e:
                print(f"Failed to upload {file_path}: {e}")
                await message.channel.send(
                    f"Failed to upload {video_title} @ {file_path}: {e}"
                )

            # Delete the file after uploading
            try:
                print(f"Deleting {file_path}")
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
                await message.channel.send(
                    f"Failed to delete {video_title} @ {file_path}: {e}"
                )

            # Delete the discord message after processing
            try:
                print(f"Deleting message {message.id}")
                await message.delete()
            except Exception as e:
                print(f"Failed to delete message: {e}")
                await message.channel.send(f"Failed to delete message: {e}")
