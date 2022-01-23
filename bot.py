import discord
from discord.ext import commands  
from discord import Member
import traceback
import sys
import datetime
import config

intents = discord.Intents.default()
intents.members = True
description='''Hello, I'm a bot written with discord.py'''

def get_prefix(bot, message):
  return ["cc.", "cc! "]

initial_extensions = (
    'cogs.commands',
    'cogs.moderation',
    'cogs.music',
)

class SomeRandomBot (commands.Bot):
    def __init__(self):
        self.uptime=datetime.datetime.utcnow()
        
        super().__init__(
            command_prefix=get_prefix,
            description=description,
            owner_id=714554283026153554,
            intents=intents,
        )
        
        self.load_extension("jishaku")
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {bot.user.name}")
        await self.change_presence(activity=discord.Game('cc.help'))
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        #ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)
        
        #if isinstance(error, ignored):
         #   return
        
        embed = discord.Embed(title="Command Error", description=f"Ignoring exception in command {ctx.command}", color=discord.Color.blue())
        embed.add_field(name="Error", value=f"`{str(error)}`")
            
        await ctx.send(embed=embed)
    
    @commands.Cog.listener('on_message')
    async def _hello(self, message):
        if message.content.startswith('hello'):
            await message.channel.send('hello')
    
bot = SomeRandomBot()

bot.help_command = commands.MinimalHelpCommand()

bot.run(config.token)
