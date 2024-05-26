import os
import discord
from dotenv import load_dotenv
from jokes import jokes
import random 
from discord.ext import commands
from weather import get_weather

load_dotenv()
TOKEN = os.getenv("TOKEN")
SERVERNAME = os.getenv("SERVERNAME")
intents = discord.Intents.default()
intents.members = True
intents =  discord.Intents.all()

bot = commands.Bot(command_prefix = "!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name = SERVERNAME)
    print(f"This channel is owned by {guild.owner}")
    print(f"Connected to'{guild.name}' server id {guild.id}")
    print(f"There are a total of {guild.member_count} members")
    print(f"Guild Members: ")
    for member in guild.members:
        print(member.name)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi, welcome to my Discord Server!")

@bot.command(name = "ping")
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command(name = "joke")
async def joke(ctx):    
    response = random.choice(jokes)
    await ctx.send(response)

@bot.command(name = "calculate")
async def calculate(ctx, expression):
    try:
        result = eval(expression)
        await ctx.send(f"Result: {result}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name = "weather")
async def weather(ctx):
    response = get_weather()
    await ctx.send(response)

bot.run(TOKEN)