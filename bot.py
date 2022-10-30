import discord
import random
import os
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.all()

client = commands.Bot(command_prefix = 'tb!', intents = intents)
status = cycle(['the album Taylor Swift','the album Fearless (Taylor\'s Version)', 'the album Speak Now', 'the album Red (Taylor\'s Version)', 'the album 1989', 'the album reputation', 'the album Lover', 'the album folklore', 'the album evermore', 'the album Midnights'])

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    change_status.start()
    print('Hi.\nTechBot is ready to use!')

@client.event
async def on_member_join(member):
    print(f'{member} has joined {member.guild.name}!')
    channel = client.get_channel(1035733930810282082)

    await channel.send(f'{member.mention} has joined **{member.guild.name}**! Welcome!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left {member.guild.name}.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Hold on! You don\'t have permission to do that in this server.')

@client.event
async def on_command_error(ctx, error):
    await ctx.send('Oops! That command doesn\'t exist. Type tb!help for a list of commands.')

@tasks.loop(seconds=7826)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball'])
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
        await ctx.send(f'You need to ask the 8 ball a question to use it!')
    else:
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(aliases=['repeat'])
async def echo(ctx, *, echotext=''):
    if echotext is '':
        await ctx.send(f'Please enter text that can be echoed.')
    else:
        await ctx.send(echotext)

@client.command(aliases=['yesorno'])
async def yesno(ctx):
    await ctx.send(random.choice(['yes', 'no']))

@client.command(aliases=['flipacoin', 'flipcoin'])
async def coin(ctx):
    await ctx.send(random.choice(['Heads.', 'Tails.']))

@client.command()
async def sleep(ctx):
    await ctx.send(random.choice(['😴', '💤']))

@client.command()
async def nothing(ctx):
    await ctx.send(f' ')

@client.command(aliases=['cls'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared 100 messages from this channel.')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason='No reason provided'):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason='No reason provided'):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} was banned.')

@client.command()
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

client.run('')
