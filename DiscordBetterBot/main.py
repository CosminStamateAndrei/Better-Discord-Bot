import discord
from discord import Intents, Profile
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
import time
import random
import requests
import bs4
import nmap
from os import path
#in-system-built    
from module import hasRole
from module import isOwner
from module import isOwnerServer

#global variables
counter = -1
mins = 0
hours = 0
debounce = 0
moreThanNine = False
#end of global variables

#arrays built as variables
memes = ['https://cdn.discordapp.com/attachments/769625535034163210/806548687232827392/2Q.png', 'https://cdn.discordapp.com/attachments/769625535034163210/806548849409261628/p072ms6r.png',
         'https://cdn.discordapp.com/attachments/769625535034163210/806548985778667530/maxresdefault.png']
#end of arrays

@tasks.loop(seconds=1)
async def counter_bot():
    global counter
    counter += 1
    return counter


client = commands.Bot(command_prefix='.')
# status = cycle(['with your expectations',
#                'the .Help command to see all the commands',
#                'Don`t forget it is a capital H in the help command'])


@client.event
async def on_ready():
    counter_bot.start()
   #change_status.start()
    reminder.start()
    print('Bot is ready!')
    print('Logs:')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="music on **SAKURA** times"))


#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.CommandNotFound):
#        return
#    if isinstance(error, commands.MissingRole):
#        await ctx.send('You don`t have the role to do that')


@tasks.loop(seconds=10)
async def change_status():
    global counter
    global mins
    global hours
    counter += 1
    if counter >= 60:
        counter = 0
        mins = mins + 1
    if mins >= 60:
        mins = 0
        hours = hours + 1

    await client.change_presence(activity=discord.Game(f'Your expectations were satisfied for {hours} hours and {mins} mins.'))
    counter = counter - 1


@tasks.loop(seconds=20000)
async def reminder():
    global debounce
    if debounce > 0:
        general_chat = client.get_channel(781822728441298985)
        await general_chat.send('For help just type ".Help".  It will give you information about me. 🕜')
        print(f'{time.asctime()}:   Reminder just reseted')
    debounce += 1


@client.command()
async def ping(ctx):
    print(f'{ctx.author.name} checked the ping at {time.asctime()}')
    await ctx.send(f'Pinged {round(client.latency * 1000)}ms')


@client.command(aliases=['c', 'cc'])
@commands.has_role('DJ')
async def clear(ctx, *, amount):
    amount = int(amount)
    print(f'{time.asctime()}:   {ctx.author.name} has cleared {amount} messages from the {ctx.channel} channel')
    await ctx.channel.purge(limit=amount+1)


@client.command(aliases=['ca', 'cca'])
@commands.has_role('DJ')
async def clearalot(ctx, amount=100):
    print(
        f'{time.asctime()}:   The member {ctx.author.name} with the id {ctx.author.id} has deleted almost all the chat in the channel: {ctx.channel}')
    await ctx.channel.purge(limit=amount)


@client.command(aliases=['ver', 'v'])
async def version(ctx):
    embed = discord.Embed(
        description='The version is alpha 0.0.1',
        colour=discord.Colour.purple()
    )
    await ctx.send(embed=embed)

@client.command(aliases=['cse'])
async def createSimpleEmbed(ctx, Title, *,Description):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(
        title = Title,
        description = Description,
        colour = discord.Colour.purple()
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')


@client.command()
async def Help(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(
        title='Help',
        description='Here you can find what you need to do in order to call commands.',
        colour=discord.Colour.red()
    )
    embed.set_footer(text='Commands that have a "*" are requiring permissions')
    embed.add_field(
        name='.ping', value='This gives you the exactly number of ms the bot has', inline=False)
    embed.add_field(
        name='.clear', value='This takes 2 parameters. First is .clear and the second is the number of messages.*', inline=False)
    embed.add_field(
        name='.clearalot', value='This clears 100 messages from the channel you are sending it. Very useful for bulk deletes*', inline=False)
    embed.add_field(
        name='.poll', value='Poll are written like this: .poll {question} - {choice1} {choice2} {choice9max}*', inline=False)
    embed.add_field(
        name='.rankshow', value='This gives you the roles of someone in the server. The syntax is like this: .rankshow @member', inline=False)
    embed.add_field(
        name='.add**TheRole**', value='You can add a role by simply typing .add**TheRole** @member', inline=False)
    embed.add_field(
        name='.version', value='It will show you the current version of the bot', inline=False)
    embed.add_field(
        name='.ship', value='You simply type .ship @member and you will be given a percent to be together with that person', inline=False)
    embed.add_field(
        name='.addAlianta', value='You can make a voice-channel for 2 separate ranks*', inline=False)
    embed.add_field(
        name='.search {LoL Name}', value='You can see your stats on Leauge of Legends by typing this command. Btw you can spell it however you like and it will work', inline=False)
    embed.set_thumbnail(
        url=ctx.author.guild.icon_url)
    await ctx.send(embed=embed)


@client.command()
async def ship(ctx, member: discord.Member):
    print(f'{time.asctime()}:   {ctx.author.name} shipped {member.name} in the {ctx.channel} channel')
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{ctx.author.mention} ships {member.mention}')
    value = random.randint(1, 100)
    if value > 0 and value <= 10:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【█---------】')
    elif value > 10 and value <= 20:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【██--------】')
    elif value > 20 and value <= 30:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【███-------】')
    elif value > 30 and value <= 40:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【████------】')
    elif value > 40 and value <= 50:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【█████-----】')
    elif value > 50 and value <= 60:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【██████----】')
    elif value > 60 and value <= 70:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【███████---】')
    elif value > 70 and value <= 80:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【████████--】')
    elif value > 80 and value <= 90:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【█████████-】')
    elif value > 90 and value <= 100:
        await ctx.send(
            f'The chances for them to be lovers is: {value}%\n【██████████】')


@client.command()
@commands.has_permissions(kick_members=True)
async def displayembed(ctx):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(
        title='Titlu',
        description='Aici e descrierea',
        colour=discord.Colour.red()
    )

    embed.set_footer(text='Acesta este un footer')
    embed.set_image(
        url='https://cdn.discordapp.com/attachments/748943736293163038/781270221637288006/1606073462735.png')
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/748943736293163038/781270221637288006/1606073462735.png')
    embed.set_author(name=ctx.author.name,
                     icon_url=ctx.author.avatar_url)
    embed.add_field(name='Numele campului', value='Valoarea campului',
                    inline=False)  # sau true daca vrei tu | se poate pune de cate ori vrei tu (pentru regulament and shit)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)




@client.command()
@commands.has_permissions(kick_members=True)
async def poll(ctx, *, answer):
    print(f'{ctx.author.name} has made a poll at {time.asctime()}')
    await ctx.channel.purge(limit=1)
    i = 1
    var = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    question = answer.split('-')
    answers = question[1].split()
    embed = discord.Embed(
        title='Poll',
        description=f'{question[0]}',
        colour=discord.Colour.red()
    )
    for ans in answers:
        embed.add_field(
            name=f'Choose {var[i-1]} for this:', value=ans)
        i += 1
        if i == 10:
            global moreThanNine
            moreThanNine = True
            break
    embed.set_author(name=ctx.author.name,
                     icon_url=ctx.author.avatar_url)
    msg = await ctx.send(embed=embed)
    for da in range(i):
        if da == 1:
            await msg.add_reaction('🇦')
        elif da == 2:
            await msg.add_reaction('🇧')  # apesi pe ctrl+p
        elif da == 3:
            await msg.add_reaction('🇨')
        elif da == 4:
            await msg.add_reaction('🇩')
        elif da == 5:
            await msg.add_reaction('🇪')
        elif da == 6:
            await msg.add_reaction('🇫')
        elif da == 7:
            await msg.add_reaction('🇬')
        elif da == 8:
            await msg.add_reaction('🇭')
        elif da == 9:
            await msg.add_reaction('🇮')
    if moreThanNine:
        await ctx.send("Those are too many words. Stretched to 9 answers. To rewrite it just press CTRL+Z on your chat box.")


@client.command()
async def rankshow(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    member_roles = member.roles
    member_roles.pop(0)
    embed = discord.Embed(
        title=f'{member.name} has those roles',
        colour=discord.Colour.purple()
    )
    contur = 1
    for role in reversed(member_roles):
        contur = str(contur)
        embed.add_field(name=contur+'.', value=role.mention,
                        inline=False)
        contur = int(contur)
        contur += 1

    await ctx.send(embed=embed)
    print(f'{ctx.author.name} just used the rankshow command. Something might pe sketchy')


@client.command(aliases=['rs'])
async def rankbettershow(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    member_roles = member.roles
    member_roles.pop(0)
    bettermr = []
    for things in reversed(member_roles):
        bettermr.append(things)
    embed = discord.Embed(
        title=f'{member.name} has those roles:',
        colour=discord.Colour.purple()
    )
    for each in bettermr:
        embed.add_field(name='⠀', value=each.mention,
                        inline=False)
    await ctx.send(embed=embed)




@client.command()
async def meme(ctx):
    await ctx.channel.purge(limit=1)
    global memes
    position = random.randint(1, len(memes)) - 1
    await ctx.send(memes[position])


@client.command()
@commands.has_role('CelMaiSarman')
async def addSarman(ctx,  member: discord.Member):
    targetRoles = member.roles
    guild = ctx.author.guild
    role = discord.utils.get(guild.roles, name='Sarman')
    try:
        targetRoles.index(role)
        await ctx.send(f'{member.mention} already has this role')
    except Exception:
        await member.add_roles(role)
        embed = discord.Embed(
            description=f'The role {role} was succesfully added to {member.mention} by {ctx.author.mention}.',
            colour=discord.Colour.purple()
        )
        print(
            f'{time.asctime()}:   {ctx.author.name} just gave {member.name} the role {role}')
        await ctx.send(embed=embed)


@client.command()
@commands.has_role('CelMaiSarman')
async def removeSarman(ctx,  member: discord.Member):
    targetRoles = member.roles
    guild = ctx.author.guild
    role = discord.utils.get(guild.roles, name='Sarman')
    try:
        targetRoles.index(role)
        await member.remove_roles(role)
        embed = discord.Embed(
            description=f'The role {role} was succesfully removed from {member.mention} by {ctx.author.mention}.',
            colour=discord.Colour.purple()
        )
        print(
            f'{time.asctime()}:   {ctx.author.name} just removed {member.name} the role {role}')
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(f'{member.name} doesn`t have the role.')


@client.command()
@commands.has_role('lider factiune')
async def addAlianta(ctx, role: discord.Role, role2: discord.Role, name):
    await ctx.channel.purge(limit=1)
    splitedName = name.split("-")
    localVoiceKing = '803557781163737108'
    if ctx.channel.id == 803554785294680094:
        await ctx.send("Loading.")
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        await ctx.send("Loading..")
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        await ctx.send("Loading...")
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        guild = ctx.guild
        categ = guild.categories
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                view_channel=False),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True),
            role: discord.PermissionOverwrite(view_channel=True),
            role2: discord.PermissionOverwrite(view_channel=True)
        }
        await guild.create_voice_channel(name=f'Alianta {name}', category=categ[2], overwrites=overwrites)
        embed = discord.Embed(
            title=f'{ctx.author.name} just created the ally channel -> `Alianta {name}`',
            description=f'Channel succesfuly created.',
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)
        print(
            f'{time.asctime()}:   {ctx.author.name} just succesfuly added the ally between {splitedName[0]} and {splitedName[1]}.')
    else:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(
            description=f'This is the wrong channel to do it, {ctx.author.mention}',
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)


@client.command()
@commands.has_role('lider factiune')
async def removeAlianta(ctx, num):
    num = int(num)
    guild = ctx.guild
    vc = guild.categories[2].voice_channels
    if ctx.channel.id == 803554785294680094:
        await ctx.channel.purge(limit=1)
        await vc[num-1].delete()
        embed = discord.Embed(
            title=f'{ctx.author.name} just removed the ally channel -> `{vc[num-1]}`',
            description=f'Channel succesfuly removed.',
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)
        print(
            f'{time.asctime()}:   {ctx.author.name} just succesfuly removed the ally.')
    else:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(
            description=f'This is the wrong channel to do it, {ctx.author.mention}',
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=embed)


@client.command(aliases=['sl'])
async def searchlol(ctx, name):
    await ctx.channel.purge(limit=1)
    name1 = name.lower()
    req = requests.get('https://u.gg/lol/profile/eun1/' + name1 + '/overview')
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    page = soup.find_all(
        class_='rank-wins')
    winRate = page[0].strong.text
    games = page[0].span.text
    summonerName = soup.find(class_='summoner-name')
    rank = soup.find(class_='rank-text')

    mainName = soup.find_all(class_='champion-name')
    mainKDA = soup.find_all(class_='champion-stats_col champion-stats_col-2')
    mainWinRate = soup.find_all(class_='win-rate')
    mainGames = soup.find_all(class_='total-games')

    embed = discord.Embed(
        title=f'The stats for {summonerName.text}',
        colour=discord.Colour.purple()
    )
    icon = soup.find('img').get('src')
    embed.set_footer(
        text=f'For more details go to https://u.gg/lol/profile/eun1/{name1}/overview')
    embed.set_author(name=ctx.author.name,
                     icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(
        url=icon)
    embed.add_field(name='Win Rate', value=winRate,
                    inline=False)
    embed.add_field(name='Games', value=games,
                    inline=False)
    embed.add_field(name='Solo Rank', value=rank.text,
                    inline=False)
    embed.add_field(name='Main Champion', value=f'**{summonerName.text}** mains **{mainName[0].text}** with **{mainKDA[0].span.text}** KDA and **{mainWinRate[0].strong.text}** win rate in **{mainGames[1].text}**',
                    inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['sy'])
async def searchyt(ctx, *, searchSubject):
    await ctx.channel.purge(limit=1)
    splitedResult = searchSubject.split()
    fakeLink = ''
    for word in splitedResult:
        fakeLink = f'{fakeLink}{word}+'
    num = len(fakeLink) - 1
    actualLink = ''
    for i in range(num):
        actualLink = f'{actualLink}{fakeLink[i]}'
    url = f'https://www.youtube.com/results?search_query={actualLink}'
    print(url)
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    print(soup)

@client.command()
async def closeClient(ctx):
    if ctx.author.id == 518331788880510979:
        await client.close()


@client.event
async def on_raw_reaction_add(ctx):
    print(ctx)
    guild = client.get_guild(748664811277254672)
    ticketRole = guild.get_role(751084722867666994)
    if ctx.channel_id == 817108438765142036 and ctx.user_id != 786515106258354206:
        isItThere = False
        channel = guild.get_channel(817108438765142036)
        message = channel.get_partial_message(817157509667880990)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True),
            ticketRole: discord.PermissionOverwrite(view_channel=True)
        }
        await ctx.member.add_roles(ticketRole)
        channels = guild.channels
        for chn in channels:
            if chn.name == f'ticket-{ctx.user_id}':
                isItThere = True
        await message.clear_reactions()
        await message.add_reaction('👍')
        if isItThere == False:
            await guild.create_text_channel(name=f'ticket-{ctx.user_id}', overwrites=overwrites)
        else:
            await ctx.member.send("You already have a ticket. If there is a problem, you can go end the ticket and you can make another-one")
            return
        ticketChannelid = None
        channs = guild.channels
        for chnl in channs:
            if chnl.name == f'ticket-{ctx.user_id}':
                ticketChannelid = chnl.id
        ticketChannel = guild.get_channel(ticketChannelid)
        embed = discord.Embed(
        title = 'Ticket',
        description = 'Scrieti aici principalele motive pentru care ati facut ticket-ul',
        colour = discord.Colour.purple()
        )
        msg = await ticketChannel.send(embed=embed)
        await msg.add_reaction('🙋')
    localTicketChannelid = None
    chans = guild.channels
    for ch in chans:
        if ch.name == f'ticket-{ctx.user_id}':
            localTicketChannelid = ch.id
    localTicketChannel = guild.get_channel(localTicketChannelid)
    if ctx.channel_id == localTicketChannelid:
        perms = discord.Permissions()
        await localTicketChannel.set_permissions(ticketRole, send_messages=False, view_channel=False)
        await ctx.member.remove_roles(ticketRole)
        statusOfTicket = discord.Embed(
        title = 'Ticket Status',
        description = 'Ticket was closed by the customer',
        colour = discord.Colour.red()
        )
        await localTicketChannel.send(embed=statusOfTicket)
        #sa vad daca merge si dupa sa pot face ceva model de aplicatie
@client.command(aliases=['dt'])
@commands.has_permissions(administrator=True)
async def deleteTicket(ctx):
    channel = ctx.channel
    ticketName = channel.name.split('-')
    if channel.name == f'ticket-{ticketName[1]}':
        await channel.delete()
        print(f'{time.asctime()}:   {ctx.author.name} just deleted the ticket named {channel.name}')

@client.command(aliases=['fu'])
async def findUser(ctx, targetIp):
    await ctx.channel.purge(limit=1)
    localMember = await ctx.guild.fetch_member(targetIp)
    if localMember != None:
        await ctx.channel.send(f'We found the member {localMember.mention}.')

@client.command()
async def test1(ctx, user: discord.Member):
    localRole = ctx.guild.get_role(778243325270294569)
    if hasRole(user, localRole):
        await ctx.channel.send('da')
    
@client.command()
async def test2(ctx, member: discord.Member):
    if isOwner(member):
        print('He is owner.')

@client.command()
async def create_mafia(ctx, colorOfMafia: discord.Color, mafiaEmoji, mafiaLider: discord.Member, *, nameOfMafia):
    guild = ctx.guild
    localGeneralRole = guild.get_role(751084724251918439)
    GeneralPermissions = localGeneralRole.permissions.value
    print('s-au luat valorile')
    await guild.create_role(name=f'{mafiaEmoji}{nameOfMafia}{mafiaEmoji}', colour=colorOfMafia, permissions=GeneralPermissions)
    roles = guild.roles
    mafiaRole = None
    for role in roles:
        if role.name == f'{mafiaEmoji}{nameOfMafia}{mafiaEmoji}':
            mafiaRole = role
    print(mafiaRole)
    print('s-a creat')

@client.command()
async def nmap(ctx, ipadress, portrange):
    try:
        nmscan = nmap.PortScanner()
        nmscan.scan(ipadress, portrange)
    except Exception:
        print('Unexpected error')

    for host in nmscan.all_hosts():
        print(f'Host: {host}{ipadress}')
        print(f'State: {nmscan[host].state()}')


@client.command()
async def eth(ctx):
    url = 'https://www.coindesk.com/price/ethereum'
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    page = soup.find_all(class_='price-large')
    await ctx.send(f'1 ETH is {page[0].text} now')

def btcf():
    url = 'https://www.coindesk.com/price/bitcoin'
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    page = soup.find_all('div', {'class':'price-large'})[0].text
    percent = soup.find_all('span', {'class':'percent-value-text'})[0].text
    print(f'1 BTC is {page} now with percentage of {percent}')

@client.command()
async def btc(ctx):
    while True:
        btcf()
        time.sleep(1)

@client.command()
async def comehere(ctx):
    voiceChannel = ctx.guild.get_channel(ctx.author.voice.channel.id)
    print(voiceChannel)
    await voiceChannel.connect()
    voice = ctx.guild.voice_client
    file = discord.File()
    voice.play(file)

@client.command(aliases = ['dc', 'dissconect'])
async def disconnect(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    await voice.disconnect()
        





client.run('')