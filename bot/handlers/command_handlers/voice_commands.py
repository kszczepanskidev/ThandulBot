import logging
from discord import PCMVolumeTransformer, FFmpegPCMAudio
from discord.ext import commands
from asyncio import get_event_loop
from youtube_dl import utils, YoutubeDL

# Join user's voice channel.
async def join_command(context):
    voice_channel = context.message.author.voice.channel

    if context.voice_client is not None:
        return await context.voice_client.move_to(voice_channel)

    await voice_channel.connect()

# Play audio from an youtube_dl supported URL, can be streamed or pre-downlaoded.
async def play_audio_command(context, url, shouldStream: bool):
    async with context.typing():
        player = await YTDLSource.from_url(url, loop=context.bot.loop, stream=shouldStream)
        context.voice_client.play(player, after=lambda e: logging.error('Player error: %s' % e) if e else None)

    await context.send(f"Now playing: {player.title} at {context.voice_client.source.volume * 100:.0f}% volume in {'loop' if context.voice_client.loop else 'single'} mode.")

# Set audio volume to given % value.
async def volume_command(context, volume):
    if context.voice_client is None:
        return logging.info('Not connected to a voice channel.')

    context.voice_client.source.volume = int(volume) / 100
    await context.send(f'Changed volume to {volume}%')

# Toggle loop option for audio player.
async def loop_command(context):
    context.voice_client.loop = not context.voice_client.loop
    await context.send(f"Playing in {'loop' if context.voice_client.loop else 'single'} mode.")

# Stop sending audio to the voice channel.
def stop_command(context):
    context.voice_client.stop()

# Stop audio and disconnect from voice channel.
async def disconnect_command(context):
    await context.voice_client.disconnect()

# Ensure connection to voice channel before invoking `yt` and `stream` commands.
async def ensure_voice(context):
    if context.voice_client is None:
        if context.author.voice:
            await context.author.voice.channel.connect()
        else:
            await context.send("You are not connected to a voice channel.")
            return logging.error("Author not connected to a voice channel.")
    elif context.voice_client.is_playing():
        context.voice_client.stop()

# Configured source for youtube_dl.
class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        # Suppress errors about console usage.
        utils.bug_reports_message = lambda: ''

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        ytdl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        ytdl = YoutubeDL(ytdl_format_options)

        loop = loop or get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        ffmpeg_options = {'options': '-vn'}

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)