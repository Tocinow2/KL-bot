import discord
import zipfile
import random
import os
from discord.ext import commands
from FunctionAI import clasificar_imagen  

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Cargar token desde variable de entorno
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot prefix y configuración
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Lista de consejos
consejos = [
    "🌱 No tengas miedo de empezar de nuevo. Es una oportunidad para hacerlo mejor.",
    "🚰 Toma agua. Muchas veces no estás cansado, estás deshidratado.",
    "🧘 Respira profundo antes de responder algo con rabia.",
    "📚 Nunca es tarde para aprender algo nuevo.",
    "🎯 No dejes que el miedo te detenga. Intenta, aunque falles.",
    "📵 Desconéctate un rato, tu mente también necesita descanso.",
    "💡 Las ideas grandes nacen en momentos tranquilos. No subestimes el silencio.",
    "🕗 Organiza tu día, pero también deja espacio para lo inesperado.",
]

# Evento cuando el bot se conecta
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# Comando para dar un consejo (embed)
@bot.command()
async def consejo(ctx):
    consejo_aleatorio = random.choice(consejos)
    embed = discord.Embed(
        title="Consejo del día",
        description=consejo_aleatorio,
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Comando de saludo
@bot.command()
async def saludo(ctx):
    await ctx.send(f"¡Hola {ctx.author.mention}! Espero que tengas un gran día 😊")

# Comando de ayuda personalizado
@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(
        title="Ayuda de KL Bot",
        description="Lista de comandos disponibles:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!consejo", value="Te da un consejo aleatorio.", inline=False)
    embed.add_field(name="!saludo", value="El bot te saluda.", inline=False)
    embed.add_field(name="!ayuda", value="Muestra este mensaje de ayuda.", inline=False)
    embed.add_field(name="!clasificar", value="Clasifica una imagen adjunta usando IA.", inline=False)  # Añade el comando a la ayuda
    await ctx.send(embed=embed)

# Comando para clasificar imágenes usando IA
@bot.command()
async def clasificar(ctx):
    if not ctx.message.attachments:
        await ctx.send("Por favor, adjunta una imagen para clasificar.")
        return

    imagen = ctx.message.attachments[0]
    img_path = f"./temp_{imagen.filename}"
    await imagen.save(img_path)

    try:
        clase, score = clasificar_imagen(img_path)
        await ctx.send(f"Clase predicha: **{clase}**\nConfianza: **{score:.2f}**")
    except Exception as e:
        await ctx.send(f"Error al clasificar la imagen: {e}")
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)

# Manejo de errores
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Ese comando no existe. Usa `!ayuda` para ver los comandos disponibles.")
    else:
        await ctx.send(f"❌ Ocurrió un error: {str(error)}")

# Ejecutar el bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ No se encontró el token en las variables de entorno. Configura DISCORD_TOKEN.")