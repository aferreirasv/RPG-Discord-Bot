from random import randrange
import re
import discord
import os
from discord.ext import commands
from discord.voice_client import VoiceClient

bot = commands.Bot(command_prefix='$',
                   description='A bot that greets the user back.')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print('Message from {0.author}: {0.content}'.format(message))
    await bot.process_commands(message)


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

print(os.environ['TOKEN'])
bot.run(os.environ['TOKEN'])