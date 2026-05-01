import discord
import subprocess
import docker
import psutil
from dotenv import load_dotenv
import os

load_dotenv("/srv/scripts/.env")
TOKEN = os.getenv("TOKEN_BOT")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connecté : {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!status":
        docker_client = docker.from_env()
        containers = docker_client.containers.list(all=True)
        response = "**Status des conteneurs :**\n"
        for c in containers:
            emoji = "✅" if c.status == "running" else "❌"
            response += f"{emoji} {c.name} - {c.status}\n"
        await message.channel.send(response)

    if message.content == "!disk":
        disk = psutil.disk_usage("/")
        storage_percent = disk.percent
        response = f"Disque utilisé à : {storage_percent} %"
        await message.channel.send(response)

    if message.content == "!ram":
        ram = psutil.virtual_memory()
        percent_usage = ram.percent
        response = f"Ram utilisé à : {percent_usage} %"
        await message.channel.send(response)

    if message.content == "!cpu":
        cpu = psutil.cpu_percent(2)
        response = f"CPU utilisé à : {cpu} %"
        await message.channel.send(response)

    if message.content == "!zombie":
        zombie = psutil.process_iter(['status'])
        nbZombie = 0
        for z in zombie :
             if z.status() == "zombie" :
                  nbZombie += 1
        response = f"Processus zombie : {nbZombie}\n"
        for z in zombie :
             response += f"PID : {z.pid}"
        await message.channel.send(response)

client.run(TOKEN)
