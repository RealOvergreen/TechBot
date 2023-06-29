import discord
import random
import os
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.all()

client = commands.Bot(command_prefix = 'tb!', intents = intents, help_command=None)
client.remove_command=('help')

class help2(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=0x006dff, description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

client.help_command = help2()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lovejoy"))    
    print('Hi.\nTechBot is ready to use!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left {member.guild.name}.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Hold on! You don\'t have permission to do that in this server.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Oops! That command doesn't exist. Type tb!help for a list of commands.")
    await ctx.send(f"Oops! An error occurred: {str(error)}.")


@client.command(brief='Shows the latency of the bot.', description='Shows the latency of the bot from when you sent your message to when the bot responds.')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball'], brief='Ask a question, and get a response from the 8 ball. 🎱', description='Ask a question, and get a response from the 8 ball. 🎱')
async def magic8ball(ctx, *, question=''):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good, try Gmail instead.",
                "Very doubtful.",
                "No.",
                "Obviously... yes.",
                "Stars say no.",
                "I don't know, try again.",
                "Obviously... no.",
                "Try again.",]
    if question is '':
        await ctx.send(f'🎱 You need to ask the 8 ball a question to use it!')
    else:
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(brief='Kicks a member from the server.', description='TechBot will kick the member provided from the server. You must have moderation powers to run this command.')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason='No reason provided'):
        await member.kick(reason=reason)

@client.command(brief='Bans a member from the server.', description='TechBot will ban the member provided from the server. You must have moderation powers to run this command.')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason='No reason provided'):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} was banned.')

@client.command(brief='Unbans a banned member from the server.', description='TechBot will unban a member that was previously banned from the server. You must have moderation powers to run this command.')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Successfully unbanned {user.mention}.')
            return

@client.command(brief='Receive a random color and a hex code for it.', description='TechBot will send an embed with a randomly picked color and the hex code for that color.')
async def color(ctx):
    r = random.randint(100000, 999999)
    e = discord.Embed(title='Random Color :rainbow:', description = f'0x{r}', color=r)
    await ctx.send(embed=e)

@client.command(brief='Receive a random number.', description='TechBot will send an embed with random number.')
async def number(ctx):
    e = discord.Embed(title='Random Number :1234:', description = (random.randint(1, 9999)), color = random.randint(100000, 999999))
    await ctx.send(embed=e) 


@client.command(aliases=['repeat'], brief='Repeats the text you sent.', description='Send some text to TechBot, and it will be repeated.')
async def echo(ctx, *, echotext=''):
    if echotext is '':
        await ctx.send(f'Please enter text that can be echoed.')
    else:
        await ctx.send(echotext)

@client.command(aliases=['yesorno'], brief='Get an answer of yes or no.', description='TechBot will tell you yes or no.')
async def yesno(ctx):
    await ctx.send(random.choice(['yes', 'no']))

@client.command(aliases=['flipacoin', 'flipcoin'], brief='A simple coin flip; you get either heads or tails.', description='TechBot flips a coin, and gives you the result of heads or tails.')
async def coin(ctx):
    await ctx.send(random.choice(['Heads.', 'Tails.']))

@client.command(brief='😴', description='TechBot sends an emoji that resembles what we should probably all get...')
async def sleep(ctx):
    await ctx.send(random.choice(['😴', '💤']))

@client.command(brief='...', description='TechBot will send... nothing. All there is to it.')
async def nothing(ctx):
    await ctx.send(f'_ _')

@client.command(aliases=['cls'], brief='Clears messages from the channel.', description='TechBot will clear messages from the channel the message was sent in.')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1000):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {(amount)} messages from this channel.')

# Enter your token between the apostrophes here.
client.run('')
