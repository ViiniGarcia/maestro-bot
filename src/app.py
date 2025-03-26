import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()
try:
    TOKEN = os.environ["DISCORD_TOKEN"]
except KeyError:
    TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


def get_r6_map_channels(bot):
    channels = []
    categories = bot.guilds[0].categories
    for category in categories:
        if category.name == "R6 - Mapas":
            for channel in category.channels:
                channels.append({channel.name: channel.id})
    return channels


# Criação da árvore de comandos
class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        # Sincroniza os comandos com o Discord
        await self.tree.sync()


# Inicialização do bot
bot = MyBot()


# Evento de inicialização do bot
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Evento de criação de comandos
@bot.tree.command(name="tatics", description="Compartilhe táticas de jogo.")
# Define os parâmetros do comando
@app_commands.describe(
    url="Link para a tática",
    game_map="Escolha o mapa",
    bomb="Escolha o local da bomba",
    operators="Escolha os operadores",
)
# Define as opções do comando
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
        app_commands.Choice(
            name="Universidade Bartlett", value="Universidade Bartlett"
        ),
        app_commands.Choice(name="Canal", value="Canal"),
        app_commands.Choice(name="Villa", value="Villa"),
        app_commands.Choice(name="Emerald Plains", value="Emerald Plains"),
        app_commands.Choice(name="Teste", value="Teste"),
    ],
    phase=[
        app_commands.Choice(name="Ataque", value="Ataque"),
        app_commands.Choice(name="Defesa", value="Defesa"),
    ],
)
# Define a função do comando
async def tatics(
    interaction: discord.Interaction,
    url: str,
    game_map: app_commands.Choice[str],
    phase: app_commands.Choice[str],
    bomb: str,
    operators: str,
):
    # Defer para evitar múltiplas respostas
    await interaction.response.defer()

    channel_ids = get_r6_map_channels(bot)
    target_channel = None
    for channel in channel_ids:
        for (
            key,
            value,
        ) in channel.items():  # Itera sobre os pares chave-valor do dicionário
            if key == game_map.value:
                target_channel = bot.get_channel(value)

    if target_channel is None:
        # Corrige a criação do canal, associando-o à categoria correta
        category = discord.utils.get(bot.guilds[0].categories, name="R6 - Mapas")
        if category is None:
            await interaction.followup.send("Categoria 'R6 - Mapas' não encontrada.")
            return
        target_channel = await bot.guilds[0].create_text_channel(
            name=game_map.value, category=category
        )

    message = f"""Mapa: {game_map.value}\nFase: {phase.value}\nBomba: {bomb}\nOperadores: {operators}\n{url}"""

    # Envia a mensagem para o canal de destino
    await target_channel.send(message)

    # Confirmação no canal de interação
    await interaction.followup.send(
        f"Mensagem enviada para o canal {target_channel.name} dentro da categoria R6 - Mapas com sucesso!"
    )


bot.run(TOKEN)
