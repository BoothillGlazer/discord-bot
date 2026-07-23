import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

SCENARIOS_CHANNEL_ID = 1527980515712434246

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user.name}")


@bot.event
async def on_message(message):
    # Ignoruj wiadomości wysłane przez boty
    if message.author.bot:
        return

    # Twórz wątki tylko na kanale scenarios
    if message.channel.id == SCENARIOS_CHANNEL_ID:
        try:
            thread_name = message.content.strip()

            # Jeśli wiadomość jest pusta (np. tylko obrazek)
            if not thread_name:
                thread_name = f"Scenariusz od {message.author.display_name}"

            # Discord pozwala maksymalnie na 100 znaków
            thread_name = thread_name[:100]

            await message.create_thread(
                name=thread_name,
                auto_archive_duration=60
            )

        except discord.Forbidden:
            print("❌ Bot nie ma uprawnień do tworzenia wątków.")

        except discord.HTTPException as e:
            print(f"❌ Nie udało się utworzyć wątku: {e}")

    # Pozwala działać komendom
    await bot.process_commands(message)


bot.run(TOKEN)
