# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 17:16:51 2020

@author: atseewal
"""

#%% Imports
import discord, os#, random, asyncio
from datetime import datetime
import numpy as np
from discord.ext import commands
from SoT_webscraping import daily_bounties
from SoT_date_parse import parse_SoT_date
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')

client=commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    
    await client.change_presence(activity = discord.Game(name='Sea of Thieves'))

@client.command(pass_context=True)
async def dailybounty(ctx):
    
    # Load the latest bounty file
    d_bounty = np.load('SoT_output.npy', allow_pickle=True).item()
    
    # Get time values
    d_bounty['Bounty_End_dt'] = parse_SoT_date(d_bounty['Bounty_End'])
    
    # Compare time values
    if d_bounty['Bounty_End_dt'] >= datetime.now():
        print('Cached challenge still active, using cached challenge')
        embed = discord.Embed(title = d_bounty['Title'], description = d_bounty['Description'], color = discord.Color.green())
        embed.add_field(name = 'Bounty End', value = d_bounty['Bounty_End'])
    elif d_bounty['Bounty_End_dt'] < datetime.now():
        print('Cached challenge expired, scraping new challenge')
        print('starting scraping')
        d_bounty = daily_bounties(os.getenv('XBOX_USERNAME'), os.getenv('XBOX_PASSWORD'))
        print('scraping complete')
        embed = discord.Embed(title = d_bounty['Title'], description = d_bounty['Description'], color = discord.Color.green())
        embed.add_field(name = 'Bounty End', value = d_bounty['Bounty_End'])
        np.save('SoT_output.npy', d_bounty)
    else:
        print('Date Error')
        embed = discord.Embed(title = 'Date error', description = 'Please contact dev', color = discord.Color.red())
    
    await ctx.send(embed=embed)

client.run(os.getenv('DISCORD_TOKEN'))
