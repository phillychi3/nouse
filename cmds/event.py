import asyncio
import datetime
import json

import discord
from core.classes import Cog_Extension, Gloable_Data
from core.errors import Errors
from discord.ext import commands


class Event(Cog_Extension):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    '''指令錯誤觸發事件'''
    Gloable_Data.errors_counter += 1
    error_command = '{0}_error'.format(ctx.command)
    if hasattr(Errors, error_command):  
      error_cmd = getattr(Errors, error_command)
      await error_cmd(self, ctx, error)
      return
    # else:  # 使用 Default Error Handler
    #   await Errors.default_error(self, ctx, error)

def setup(bot):
  bot.add_cog(Event(bot))
