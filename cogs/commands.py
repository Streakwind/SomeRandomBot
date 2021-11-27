from discord.ext import commands
import discord
import traceback
import datetime
import humanize
from humanize import precisedelta
import sys
import typing

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def time_left(self, ctx):
        date=datetime.datetime(2022, 9, 1, hour=8, minute=30, second=0)
        humanized_version=precisedelta(date)
    
        await ctx.send(f"{humanized_version} left")
    
    @commands.is_owner()
    @commands.command(hidden=True)
    async def reload(self, ctx, extension):
        """Reload an extension"""
        try:
            self.bot.reload_extension(extension)
            print(f"{extension} successfully reloaded.")
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)
        except Exception as e:
            # this next line formats the traceback and sends it
            error = "".join(traceback.format_exception(type(e), e, e.__traceback__, 1))
            return await ctx.send(f"Failed to reload extension.\n```{error}```")
    
    @commands.command()
    async def prefix(self, ctx):
        """Prefixes for the bot"""
        await ctx.send("Prefixes: `cc.`, `cc!`")
    
    @commands.command(aliases=["latency"])
    async def ping(self, ctx):
        """The bots ping/latency"""
        
        ping = self.bot.latency * 1000
        
        ping = int(ping)
        await ctx.send(f"My ping is {ping}ms")
    
    @commands.command(aliases = ["ui"])
    async def userinfo(self, ctx, *, member: discord.Member = None):
        """Information about a certain user"""
        
        if not member:
            member = ctx.author
        
        embed = discord.Embed(title="ALL TIMES ARE IN UTC", description="", color=discord.Color.blue())
        embed.set_author(name=f"{member} - {member.id}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
         
        time=precisedelta(member.created_at, minimum_unit="hours")
        
        embed.add_field(name="User created at", value=f"{time} ago", inline=True)
        
        if ctx.guild: 
            if member in ctx.guild.members:
                time_1=precisedelta(member.joined_at, minimum_unit="hours")
                
                embed.add_field(name="User joined at", value=f"{time_1} ago", inline=True)
            else:
                embed.description += f"\nThis user ({member}) is not in the guild"
        
        if member.bot:
            embed.description += "\nThis user is a bot"
            
        if ctx.guild:     
            if member.id == ctx.guild.owner.id:
                embed.description += f"\nThis user owns this server ({ctx.guild.name})"
        if member.id == self.bot.owner_id:
            embed.description += "\nThis user owns the bot"
            
        await ctx.send(embed = embed)
    
    @commands.command()
    async def avatar(self, ctx, *, user: discord.User = None):
        """Shows you a specific users avatar"""

        if not user:
            user = ctx.author

        embed = discord.Embed(title=user, description="", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar_url)

    @commands.command()
    async def uptime(self, ctx):
        uptime_before = datetime.datetime.utcnow() - self.bot.uptime
        
        uptime = precisedelta(uptime_before)
        
        await ctx.send(f"I booted up {uptime} ago")
        
def setup(bot):
    bot.add_cog(Commands(bot))
