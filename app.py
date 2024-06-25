import discord
import asyncio
from discord.ext import commands

from fonction import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
playlist_lock = asyncio.Lock()
music_queue = []

#TOKEN

with open("TOKEN.txt","r") as file:
    TOKEN=file.read()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Music bot V2, by BerretMan"))


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Tropical Symphonie V2", description="Discord bot music, by BerretMan", color=0x00ff00)
    embed.add_field(name="!join", value="Rejoins le vocal", inline=False)
    embed.add_field(name="!add", value="Ajoute une music à la playlist", inline=False)
    embed.add_field(name="!start", value="Joue la playlist", inline=False)
    embed.add_field(name="!pause", value="Met en pause la music", inline=False)
    embed.add_field(name="!unpause", value="Stop la pause", inline=False)
    embed.add_field(name="!next", value="Passe à la musique suivante", inline=False)
    embed.add_field(name="!album(album, numéro)", value="Joue une music d'un album. Si i=-1, joue tout l'album", inline=False)
    await ctx.send(embed=embed)


async def change_activites(status):
    if status == "idle":
        message = f"TropicalSymphonie V2, by BerretMan"
    elif len(music_queue) > 0:
        if status == "play":
            message = f"▶️ {music_queue[0].name}, by BerretMan"
        elif status == "pause":
            message = f"⏸️ {music_queue[0].name}, by BerretMan"
    else:
        message = f"TropicalSymphonie V2, by BerretMan"
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(message))

@bot.command()
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    global vc
    vc = await voice_channel.connect()
    await ctx.send("🗣️Vocal rejoins")

# play single music of an album 
async def play_a_music(ctx, music):
    vc.play(discord.FFmpegPCMAudio(f"music/AI_Cocktail/{music.filename}"))
    await change_activites("play")

@bot.command()
async def start(ctx, path="music/None/"):
    async with playlist_lock:
        while len(music_queue) > 0:
            music = music_queue[0]
            vc.play(discord.FFmpegPCMAudio(source=f"{path}{music.filename}"), after=lambda e: bot.loop.call_soon_threadsafe(next_song.set))
            await change_activites("play")
            await ctx.send(f"Playing **{music.name}** by {music.author}")

            next_song = asyncio.Event()
            await next_song.wait()

            music_queue.pop(0)

    await change_activites("idle")
    await ctx.send("Playlist finished")

@bot.command()
async def unpause(ctx):
    vc.resume()
    await ctx.send(f'▶️ {music_queue[0]}')
    await change_activites("play")

@bot.command()
async def pause(ctx):
    vc.pause()
    await ctx.send(f'⏸️ {music_queue[0]}')
    await change_activites("pause")

@bot.command()
async def next(ctx):
    if vc.is_playing() or vc.is_paused():
        vc.stop()
    await ctx.send("Skipping to the next song")
    await asyncio.sleep(1)
    await start(ctx)

@bot.command()
async def album(ctx, album_name):
    music_queue.clear()
    if play_album(album_name):
        await ctx.send(f"Lancement de {album_name}\n")
        print_str = '\n'.join(f"{i + 1}- {m.name}, {m.author}" for i, m in enumerate(music_queue))
        await start(ctx, f"music/{album_name}/")
    else:
        await ctx.send("nom d'album incorect")

@bot.command()
async def add(ctx, link):
    music = download_yt(link)
    music_queue.append(music)
    await ctx.send(f"{music.name} ajouté à la file")


@bot.command()
async def clear(ctx):
    clear_None()
    clear_bdd("Youtube")
    await ctx.send(f"🗑️ La base de donnée a été clear")


bot.run(TOKEN)
