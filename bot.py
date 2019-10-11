from random import randrange
import re
import discord
import os
import requests
import json
from discord.ext import commands
from discord.voice_client import VoiceClient
from sheets.common import CommonSheet

bot = commands.Bot(command_prefix='$',
                   description='A bot that greets the user back.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


SHEET_TYPES = {"common": CommonSheet}
sheets = []

def get_author_sheet(author):
    for sheet in sheets:
        if author.id == sheet.user_id:
            return sheet
    return None        


######### TO DO ##################################################################
## Verificar se o usuário já inicializou o ciclo de criação de ficha            ##
## pelo chat do servidor da maneira correta antes de enviar a próxima pergunta  ##
##################################################################################
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    channel = message.channel
    author = message.author
    await bot.process_commands(message)
    if isdm(message) is True:
        sheet = get_author_sheet(author)
        if sheet is not None:
            field = sheet.get_next_field()
            sheet.set_field(field, message.content)
            question = sheet.get_next_question()
            if question is None:
                print(json.dumps(sheet.to_dict()))
                r = requests.post('http://localhost:3000/sheets', data=json.dumps(sheet.to_dict()), headers={"content-type":"application/json"})   
                sheets.pop(0)
                print(r.text)
                await channel.send(r.text)
            else:
                await channel.send(question)
        else:
            if message.content not in SHEET_TYPES.keys():
                return print("nope tambem")
            Sheet_Constructor = SHEET_TYPES[message.content]
            if Sheet_Constructor is None:
                return print("Nope")
            sheet = Sheet_Constructor(author.id)
            sheets.append(sheet)
            question = sheet.get_next_question()
            await channel.send(question)
    else:
        return

def isdm(message):
    if message.guild is None:
        return True
    else: 
        return False

@bot.command()
async def roll(ctx, arg, *kwargs):
    DICES = [4, 6, 8, 12, 20]
    
    arg += ''.join(map(str, kwargs))

    print(arg)
    if "d" in arg:
        match = re.match('(\d+)d(\d+)(\+|\-)(\d+)?.*', arg, flags=re.IGNORECASE)
        if match:
            full_match = match.group(0)
            num_dices = int(match.group(1))
            dice = int(match.group(2))
            sign = match.group(3)
            mod = int(match.group(4)) if match.group(4) else None
            print('{0} {1} {2} {3}'.format(num_dices, dice, sign, mod))
            if dice in DICES:
                rolls = roll_dice(dice, num_dices)
                return await ctx.send(string_build(rolls, num_dices, dice, sign, mod))
                
    return await ctx.send('Selecione um dado valido')

def roll_dice(dice, num_dices=1):
    r = []
    for i in range(num_dices):
        r.append(randrange(dice)+1)
    return r

def string_build(rolls, num_dices, dice, sign, mod):
    rolls_sum = sum(rolls)
    result_str = ''
    if mod:
        result = rolls_sum + mod if sign == '+' else rolls_sum - mod
        print(result)
        print(len(rolls))
        if len(rolls) > 1:
            for i in range(len(rolls)):
                print(i)
                r = rolls[i]
                if i == len(rolls) - 1:
                    result_str += '``r{0}`` {1} = {2}'.format(i+1, r, rolls_sum)
                else:
                    result_str += '``r{0}`` {1} + '.format(i+1, r)
        else:
            result_str = '``r1`` {0}'.format(rolls_sum)
        result_str = result_str + ' {0} ``mod`` {1} = {2}'.format(sign, mod, mod + rolls_sum)        
    else:
        print("else")
        result_str = '``r1``{0}'.format(rolls_sum)
    
    return result_str


@bot.command()
async def create_sheet(ctx, *args):
    
    message = ctx.message
    author = message.author
    dm_channel = author.dm_channel
    if dm_channel is None:
        dm_channel = await author.create_dm()
    await dm_channel.send('Selecione o tipo da ficha que seleciona criar \n 1 - common')
     

print(os.environ['DISCORD_TOKEN'])
bot.run(os.environ['DISCORD_TOKEN'])