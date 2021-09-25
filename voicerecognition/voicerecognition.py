from redbot.core import commands

async def changeSelfDeafen(ctx, state):
    channel = ctx.voice_client.channel
    await ctx.guild.change_voice_state(channel=channel, self_deaf=state)

class VoiceRecognition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.mute = True

    # Para cada comando 
    async def voiceMiddleware(self, ctx, error, success):
        isUserInVoice = hasattr(ctx.author.voice, 'channel')
        isBotPresent = self.active

        if not isUserInVoice :
            await ctx.send("You are not in a voice channel.")
        else:
            if not isBotPresent:
                self.active = True
                author = ctx.message.author
                channel = author.voice.channel
                await channel.connect()
            else:
                voiceChannelMatch = ctx.author.voice.channel == ctx.voice_client.channel
                if (voiceChannelMatch):
                    await success()
                else:
                    await error()

    # [p] means command prefix
    # when user uses [p]toggle
    @commands.command()
    async def toggle(self, ctx):

        async def error():
            await ctx.send("We are not in the same voice channel.")
            
        async def success():
            self.mute = not self.mute
            await changeSelfDeafen(ctx, self.mute)
            await ctx.send("Voice recognition enabled." if self.active else "Voice recognition disabled.")

        await self.voiceMiddleware(ctx, error, success)

    # when user uses [p]exit
    @commands.command()
    async def exit(self, ctx):

        async def error():
            await ctx.send("I am not in a voice channel.")

        async def success():
            await ctx.voice_client.disconnect()
            self.active = False

        await self.voiceMiddleware(ctx, error, success)
        