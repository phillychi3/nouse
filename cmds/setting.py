import discord
from discord.ext import commands
import os
import json
import numpy as np
import requests
class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def automod(self,ctx):
        server=ctx.guild.id

        try:
            with open(f'servers\{server}.json', 'r', encoding='unicode_escape') as jfile:
                data = json.load(jfile)     


            status=data["server"]["enable"]

            if status=="yes": 
                data["server"]["enable"]="no"
                await ctx.send("automod off")
            else:
                data["server"]["enable"]="yes"
                await ctx.send("automod on")

            with open(f'servers\{server}.json', 'w',encoding='unicode_escape') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            
        except: 

            

            data={"data":{}}
            data["server"]={}
            data["server"]["enable"]="yes"
            data["server"]["status"]="null"
            data["server"]["allmsg"]=0
            data["server"]["allmember"]=ctx.guild.member_count
            data["server"]["allchannls"]=len(ctx.guild.channels)
            data["server"]["message_text"]=[]
            data["server"]["message_id"]=[]
            data["server"]["message_text_id"]=[]
            data["server"]["message_time"]=[]
            with open(f'servers\{server}.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            await ctx.send("automod: on")

            #await ctx.send("設定過程中如遇上任何問題可進入https://discord.gg/gjX8vBn9Kv 或是使用dd.co [遇到問題] 來連絡作者")

def setup(bot):
    bot.add_cog(Live(bot))