import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

SCENARIOS_CHANNEL_ID = 1527980515712434246  # <-- Wklej tutaj ID kanału "scenarios"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user.name}")

@bot.event
async def on_message(message):
    # Ignoruj wiadomości botów
    if message.author.bot:
        return

    # Sprawdź, czy wiadomość została wysłana na kanale scenarios
    if message.channel.id == SCENARIOS_CHANNEL_ID:
        try:
            await message.create_thread(
                name=f"Scenariusz - {message.author.display_name}",
                auto_archive_duration=60
            )
        except discord.Forbidden:
            print("❌ Bot nie ma uprawnień do tworzenia wątków.")
        except discord.HTTPException as e:
            print(f"❌ Wystąpił błąd podczas tworzenia wątku: {e}")

    # Pozwala działać komendom
    await bot.process_commands(message)


bot.run(TOKEN)