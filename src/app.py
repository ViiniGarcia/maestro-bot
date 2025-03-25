import os
import discord
import requests
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        # Sincroniza os comandos com o Discord
        await self.tree.sync()

bot = MyBot()
active_games = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="tatics", description="Compartilhe táticas de jogo.")
@app_commands.describe(
    url="Link para a tática",
    game_map="Escolha o mapa",
    bomb="Escolha o local da bomba",
    operators="Escolha os operadores"
)
@app_commands.choices(
    game_map=[
        app_commands.Choice(name="Banco", value="Banco"),
        app_commands.Choice(name="Casa", value="Casa"),
        app_commands.Choice(name="Arranha-céu", value="Arranha-céu"),
        app_commands.Choice(name="Chalé", value="Chalé"),
        app_commands.Choice(name="Consulado", value="Consulado"),
        app_commands.Choice(name="Fronteira", value="Fronteira"),
        app_commands.Choice(name="Litoral", value="Litoral"),
        app_commands.Choice(name="Oregon", value="Oregon"),
        app_commands.Choice(name="Outback", value="Outback"),
        app_commands.Choice(name="Parque Temático", value="Parque Temático"),
        app_commands.Choice(name="Arranha-céu", value="Arranha-céu"),
        app_commands.Choice(name="Clube", value="Clube"),
        app_commands.Choice(name="Café Dostoiévski", value="Café Dostoiévski"),
        app_commands.Choice(name="Fortaleza", value="Fortaleza"),
        app_commands.Choice(name="Universidade Bartlett", value="Universidade Bartlett"),
        app_commands.Choice(name="Canal", value="Canal"),
        app_commands.Choice(name="Villa", value="Villa"),
        app_commands.Choice(name="Emerald Plains", value="Emerald Plains")
    ],
    phase=[
        app_commands.Choice(name="Ataque", value="Ataque"),
        app_commands.Choice(name="Defesa", value="Defesa")
    ]
)
async def tatics(
        interaction: discord.Interaction,
        url: str,
        game_map: app_commands.Choice[str],
        phase: app_commands.Choice[str],
        bomb: app_commands.Choice[str],
        operators: str
    ):
    await interaction.response.send_message(
        f"Mapa: {game_map.value}\nFase: {phase.value}\nBomba: {bomb.value}\nOperadores: {operators.value}\n{url}"
    )

bot.run(TOKEN)