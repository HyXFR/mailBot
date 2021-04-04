import yaml
import discord
from discord.ext import commands
import asyncio

# Config Init
yaml_file = open("config.yaml", 'r')
yaml_content = yaml.load(yaml_file)

for key, value in yaml_content.items():
    if key == "token":
        _token = value
    elif key == "channel_id_to_send":
        _citd = value
    elif key == "guild_id_to_send":
        _gits = value
    elif key == "prefix":
        _prefix = value

# Bot Init
bot = commands.Bot(command_prefix=_prefix)
bot.remove_command("help")
token_openned = []

# Bot
@bot.event
async def on_ready():
    print("[Bot] Connected !")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "":
        return
    
    if not message.guild:
        uctx = await bot.get_context(message)
        print(str(dmed_open))
        guild = bot.get_guild(_gits)
        channel = discord.utils.get(guild.text_channels, name="mailbot")
        if message.author.id not in token_openned:
            token_openned.append(message.author.id)
            print("[MailBot User] Received new ticket id " + str(message.author.id) + " Contain : " + message.content)
            await uctx.send("You have successfull create a ticket ! User `close` to close it !")
            await channel.send(f"[{message.author.id}] has create a ticket, content : " + message.content)
        else:
            if message.content == "close":
                token_openned.remove(message.author.id)
                print("[MailBot User] User " + str(message.author.id) + " closed his ticket")
                await uctx.send("Your ticket are successfull closed !")
                await channel.send(f"[{message.author.id}] has closed his ticket !")
            else:
                print("[MailBot User] User " + str(message.author.id) + " has sent " + message.content)
                await channel.send(f"[{message.author.id}]> " + message.content)
    await bot.process_commands(message)

@bot.command(aliases=["r"])
async def reply(ctx, id, *message):
    message = " ".join(message)
    id = int("".join(id))
    if id not in token_openned:
        print("[MailBot Staff] " + str(ctx.author.id) + " tryed to reply the ticket " + str(id) + " with message " + str(message))
        msg = ctx.send(ctx.author.name + ", This ticket don't exist.")
        await asyncio.sleep(5)
        await msg.delete()
    
    else:
        user = bot.get_user(id)
        if message == "close":
            print("[MailBot Staff] " + str(ctx.author.id) + " has close the ticket id " + str(id))
            token_openned.remove(id)
            await uctx.send("Your ticket is close. All messages will start a new !")
        else:
            print("[MailBot Staff] " + str(ctx.author.id) + " has sent a respond tu user " + str(id) + " : " + str(message))
            await uctx.send("[" + ctx.author.name + "] " + message)
            

bot.run(_token)
