import asyncio
import datetime
import json
import time
import uuid
from collections import Counter

import discord
from core.classes import Cog_Extension, Gloable_Data
from core.errors import Errors
from discord.ext import commands


class Event(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot


    def addban(self,id,baname):
        with open(f'./ban/ban.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

        try:
            id == data[str(id)]       
            data[str(id)][baname]+=1
            with open(f'./ban/ban.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4) 

        except:
            with open(f'./ban/ban.json', 'r',encoding='utf-8') as f:
                jfile = json.load(f)
            jfile[id] = {}                   
            jfile[id]["nouse"] = 0
            jfile[id]["swipe"] = 0
            jfile[id]["delete"] = 0   
            jfile[id][baname]+=1

            with open(f'./ban/ban.json', 'w') as f:
                json.dump(jfile, f, ensure_ascii=False, indent=4)

    def ban(self,id):
        with open(f'./ban/ban.json', 'r',encoding='utf-8') as f:
            data = json.load(f)
        if data[str(id)]["nouse"] >= 5:
            return "由於發送訊息過快，你現在應該要被kick了，只是有人懶得寫kick"
        if data[str(id)]["swipe"] >= 3:
            return "由於刷頻過多，你現在應該要被kick了，只是有人懶得寫kick"
        if data[str(id)]["delete"] >= 2:
            return "由於異常刪除頻道過多，你現在應該要被kick了，只是有人懶得寫kick"
   

    @commands.Cog.listener()
    async def on_message(self, msg):
        # try:
        if msg.content!="":
            server=msg.guild.id
            with open(f'servers\{server}.json', 'r', encoding='unicode_escape') as jfile:
                data = json.load(jfile)
            if data["server"]["enable"]=="yes":
                message_text=data["server"]["message_text"]
                message_id=data["server"]["message_id"]
                message_text_id=data["server"]["message_text_id"]
                message_time=data["server"]["message_time"]
                
                if len(message_text) >= 10:
                    del message_text[0]
                if len(message_id) >= 10:
                    del message_id[0]
                if len(message_text_id) >= 10:
                    del message_text_id[0]
                if len(message_time) >= 10:
                    del message_time[0]
                message_text.append(msg.content)
                message_text_id.append(msg.id)
                message_id.append(msg.author.id)
                message_time.append(time.time())
                data["server"]["message_text"]=message_text
                data["server"]["message_id"]=message_id
                data["server"]["message_text_id"]=message_text_id
                data["server"]["message_time"]=message_time
                data["server"]["allmsg"]=int(data["server"]["allmsg"])+1
                with open(f'servers\{server}.json', 'w',encoding='unicode_escape') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)


                if message_time[len(message_time)-1]-message_time[len(message_time)-2]<0.5 and message_id[len(message_id)-1]==message_id[len(message_id)-2]!=862884526903263232 :
                    await msg.channel.set_permissions(msg.guild.default_role, send_messages=False)
                    uuid4=uuid.uuid4()
                    await msg.channel.send(f"警告 刷頻行為禁止 ID:`{uuid4}`")
                    self.addban(message_id[len(message_id)-1],"nouse")
                    self.ban(message_id[len(message_id)-1])
                    await asyncio.sleep(3)
                    await msg.channel.set_permissions(msg.guild.default_role, send_messages=True)   


                if len(message_text) == 10:
                    retext=Counter(message_text)
                    reid=Counter(message_id)

                    for i in reid:

                        if reid[i]>3:                
                            reidbool=True
                            break
                        else:
                            reidbool=False

                    for i in retext:

                        if retext[i]>=4 and data["server"]["status"]!="doing" and reidbool==True:

                            with open(f'servers\{server}.json', 'r', encoding='unicode_escape') as jfile:
                                data = json.load(jfile)

                            data["server"]["status"]="doing"

                            with open(f'servers\{server}.json', 'w',encoding='unicode_escape') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)


                            global warring
                            warring=i

                            await msg.channel.set_permissions(msg.guild.default_role, send_messages=False)

                            for j in range(len(message_text)):
                                print(message_text)
                                if message_text[j] == i :
                                    try:
                                        print("susses")
                                        de = await msg.channel.fetch_message(message_text_id[j])
                                        await de.delete()


                                    except:
                                        print("error")
                            

                            print(f"-- {i}--{retext[i]}")
                            uuid4=uuid.uuid4()
                            await msg.channel.send(f"發現威脅 威脅等級:1 ID:`{uuid4}`")
                            with open(f'servers\{server}.json', 'r', encoding='unicode_escape') as jfile:
                                data = json.load(jfile)
                            data["server"]["message_text"]=[]
                            data["server"]["message_id"]=[]
                            data["server"]["message_text_id"]=[]
                            data["server"]["message_time"]=[]
                            data["server"]["status"]="null"
                            with open(f'servers\{server}.json', 'w',encoding='unicode_escape') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)

                            await msg.channel.set_permissions(msg.guild.default_role, send_messages=True)   
                            break

            else:
                pass
        else:
            print("image")





 






        # except:
        #     print("no start")

        # print(msg)
        # print(msg.channel)
        # print(msg.author)

def setup(bot):
    bot.add_cog(Event(bot))
