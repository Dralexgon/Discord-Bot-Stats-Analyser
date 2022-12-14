#This is a discord bot made by Dralexgon.
#He store all messages in a database and can do some stuff with it.

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import asyncio
import time

from Bot import Bot
from Log import Log

#intents = discord.Intents.default()
#intents.members = True
client = commands.Bot(command_prefix = "!", help_command=None, intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    Bot.init(client)
    Log.print("Bot is ready!")

@client.command(name="help", help="Shows this message.")
async def help(ctx):
    embed = discord.Embed(
        title = "Help",
        colour = discord.Colour.blue()
    )
    commandListinversed = []
    for command in client.commands:
        commandListinversed.append(command)
    for command in commandListinversed:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(ctx.author.mention, embed=embed)

@client.command(pass_context = True, name="ping", help="Answers with pong, to check if the bot is online.")
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")

@client.command(pass_context = True, name="test", help="To test stuff. (Only for Dralexgon)")
async def test(ctx: commands.Context):
    if ctx.author.id != 645005137714348041:
        await ctx.send("Only for Dralexgon !")
        return
    for guild in client.guilds:
        for member in guild.members:
            await ctx.send(f"{member.name}#{member.discriminator} is {member.status} in {guild.name}")

@client.command(pass_context = True, name="most_active", aliases=["top10"], help="This command will send the 10 most active users in the server.")
async def most_active(ctx: commands.Context):
    result = Bot.get_most_active_user(ctx.guild.name)
    embed = discord.Embed(
        title = "Top 10 most active users",
        colour = discord.Colour.blue()
    )
    for i in range(len(result)):
        embed.add_field(name=f"{result[i][0]}#{result[i][1]:0>4d}", value=f"{result[i][2]}  messages", inline=False)
    await ctx.send(ctx.author.mention, embed=embed)

@client.command(pass_context = True, name="most_use_letter", aliases=["top10letter"], help="This command will send the 10 most used letters in the server.")
async def most_use_letter(ctx: commands.Context):
    result = Bot.get_most_use_letter(ctx.guild.name)
    embed = discord.Embed(
        title = "Top 10 most used letters",
        colour = discord.Colour.blue()
    )
    for letter, value in result.items():
        embed.add_field(name=letter, value=f"{value}  times", inline=False)
    await ctx.send(ctx.author.mention, embed=embed)

@client.event
async def on_message(message : discord.Message):
    #All non-bot or non-command messages will be stored in a database.
    if message.content.startswith(client.command_prefix):
        await client.process_commands(message)
        return
    if message.author.name == client.user.name:
        return
    Bot.store_message(message)

@tasks.loop(seconds=60)#note for me, use store_users_status.start() to call it
async def store_users_status():
    for guild in client.guilds:
        for member in guild.members:
            Bot.store_user_status(member.name, member.discriminator, guild.name, member.status)

@tasks.loop(seconds=60)
async def store_users_activity():
    for guild in client.guilds:
        for member in guild.members:
            if member.activity is not None:
                Bot.store_user_activity(member.name, member.discriminator, guild.name, member.activity.name, member.activity.type.name)

    
#note, if you want to run this code, you need to create a file called token.txt one directory above the code and put your token in it.
token = open('../token.txt', 'r').readlines()[0]
client.run(token)




#note for me,
#if I want to use slash commands,
#search on this link : https://discord-interactions.readthedocs.io/en/latest/quickstart.html