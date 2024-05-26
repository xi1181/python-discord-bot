import os
import discord
from dotenv import load_dotenv
from jokes import jokes
import random 

load_dotenv()
TOKEN = os.getenv("TOKEN")
SERVERNAME = os.getenv("SERVERNAME")
intents = discord.Intents.default()
intents.members = True
intents =  discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = discord.utils.get(client.guilds, name = SERVERNAME)
    print(f"This channel is owned by {guild.owner}")
    print(f"Connected to'{guild.name}' server id {guild.id}")
    print(f"There are a total of {guild.member_count} members")
    print(f"Guild Members: ")
    for member in guild.members:
        print(member.name)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi, welcome to my Discord Server!")

@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == client.user:
        return
    print(message.content)
    if message.content == 'ping':
        await message.channel.send('pong')
    
    if message.content.startswith("joke"):
        response = random.choice(jokes)
        await message.channel.send(response)

    if message.content.startswith("calculate"):
        expression =  message.content[len("calculate"):].strip()
        try:
            result = eval(expression)
            await message.channel.send(f"Result: {result}")
        except Exception as e:
            await message.channel.send(f"Error: {e}")




client.run(TOKEN)