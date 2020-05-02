from discord.ext import commands

from ..helpers import should_perform_command
from ..command_handlers.voice_commands import join_command, play_audio_command, volume_command, loop_command, stop_command, disconnect_command, ensure_voice

class MusicCommands(commands.Cog):
    """
    Commands used to play music into voice channel.

    Usable only by users specified in environment configuration.
    """

    @commands.command(name='join')
    async def join(self, context):
        """
        Joins a voice channel of user that invoked the command.
        
        Usable only by users specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await join_command(context)

    @commands.command(name='yt')
    async def yt(self, context, url):
        """
        Plays predownloaded audio from provided URL.

        Parameters:
            - url: url to predownload and play audio from. URL must be supported by youtube_dl.
        
        Usable only by users specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await play_audio_command(context, url, shouldStream=False)

    @commands.command(name='stream')
    async def stream(self, context, url):
        """
        Streams audio from provided URL.

        Parameters:
            - url: url to stream audio from. URL must be supported by youtube_dl.
        
        Usable only by users specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await play_audio_command(context, url, shouldStream=True)

    @commands.command(name='volume')
    async def volume(self, context, volume):
        """
        Sets audio volume to given % value.

        Parameters:
            - volume: percent value to set player's volume to.
        
        Usable only by users specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await volume_command(context, volume)

    @commands.command(name='loop')
    async def loop(self, context):
        """
        Toggles loop option for audio player.
        
        Usable only by users specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await loop_command(context)

    @commands.command(name='stop')
    async def stop(self, context):
        """
        Stops sending audio to the voice channel.
        
        Usable only by users specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await stop_command(context)

    @commands.command(name='disconnect')
    async def disconnect(self, context):
        """
        Stops audio and disconnects from voice channel
        
        Usable only by users specified in environment configuration.
        """
        if not should_perform_command(context):
            return

        await disconnect_command(context)

    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, context):
        """
        Ensure connection to voice channel before invoking `yt` and `stream` commands.
        """
        await ensure_voice(context)