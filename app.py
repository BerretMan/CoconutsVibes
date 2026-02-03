import discord,os,re
import asyncio
from discord import app_commands 

from yt_dlp import YoutubeDL
from lefile import File 
from button import Button
from Bot import Bot
from Message import Message
from copy import deepcopy


MUSIC_FILE = File()
ID = 908732286978113568
GUILD_ID = discord.Object(id=ID)


intents = discord.Intents.all()
intents.message_content = True
message = Message()

def get_token():
    with open("TOKEN","r") as f:
        TOKEN = f.read()
    return TOKEN


bot = Bot(command_prefix="!", intents=intents)


async def change_statut(music):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=music))


@bot.tree.command(name="join",description=message.fjoin,guild=GUILD_ID)
async def join(interaction: discord.Interaction):
    print(f"DEBUG: Voice state de l'user : {interaction.user.voice}")

    if interaction.user.voice:
        c = interaction.user.voice.channel 
        bot.vc = await c.connect()
        await interaction.response.send_message(message.joinChannel)
    else:
        await interaction.response.send_message(message.noChannel)


@bot.tree.command(name="leave",description=message.fleave,guild=GUILD_ID)
async def leave(interaction: discord.Interaction):

    if interaction.user.voice:
        bot.vc = interaction.guild.voice_client
        await bot.vc.disconnect()
        await interaction.response.send_message(message.leaveChannel)
        return

    else:
        await interaction.response.send_message(message.noChannel)



@bot.tree.command(name="add",description=message.fadd,guild=GUILD_ID)
async def add(interaction: discord.Interaction, music: str):
    
    music = music.split("&list=")[0]
    music = music.split("&radio=")[0]
    music = music.split("&start_radio=")[0]

    print(music)
    await interaction.response.defer(ephemeral=True)
    
    option_ydl = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "nocheckcertificate":True,
            "playlist_items": "1",
            "noplaylist": True,
            "extra_param": ["--js-runtimes", "node"]
        }
    
    with YoutubeDL(option_ydl) as ydl:

        info = ydl.extract_info(music, download=False)
         
        video = info["entries"][0] if "entries" in info else info
        video_id = video.get('id')
        video_title = re.sub(r'[\\/*?:"<>|]', "", video.get('title', 'Unknown'))
    
    file_name =f"{video_id}@{video_title}.mp3" 


    if file_name in os.listdir("Music/Youtube/"):
        MUSIC_FILE.enfiler(file_name)
        await interaction.followup.send(message.download)
    else:
        await interaction.followup.send(message.downloading)
        ydl_opts = {'format': 'bestaudio/best','outtmpl': f'Music/Youtube/{video_id}@{video_title}.%(ext)s','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320',}],}

        with YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [music])
            await interaction.edit_original_response(content=message.download)

        MUSIC_FILE.enfiler(file_name)

    
def play_next(error=None):
    if not MUSIC_FILE.est_vide() and not bot.isGoto:
        music = MUSIC_FILE.defiler()
        bot.vc.play(discord.FFmpegPCMAudio(source=f"Music/Youtube/{music}"),after=play_next)
        music_name = music.split('@')[1].replace(".mp3","")
        bot.loop.create_task(change_statut(music_name))


@bot.tree.command(name="start",description=message.fstart,guild=GUILD_ID)
async def start(interaction: discord.Interaction):
    bot.vc = interaction.guild.voice_client

    if not MUSIC_FILE.est_vide():
        music = MUSIC_FILE.defiler()
        bot.current_music=music
        bot.vc.play(discord.FFmpegPCMAudio(source=f"Music/Youtube/{music}"),after=play_next)
        view = Button(bot.vc,MUSIC_FILE,music)
        music_name = music.split('@')[1].replace(".mp3","")
        await interaction.response.send_message(f"{music_name} play",view=view,ephemeral=True)
        await change_statut(music_name)
    else:
        await interaction.response.send_message(message.noMusic,ephemeral=True)


#support de trois formats
# -> 5 (nombre de s)
# -> 2m3s 
# -> 12:20
@bot.tree.command(name="goto",description=message.fgoto,guild=GUILD_ID) 
@app_commands.describe(
        timecode="Le timecode sous 3 formats: 125 (nombre de seconde) 2m5s; 2:5 (ou 02:05)"
)
async def goto(interaction: discord.Interaction, timecode:str):
    bot.isGoto=True
    temps=0
    if 'm' in timecode:
        

        number = re.search(r'(?:(\d+)m)?(?:(\d+)s)?', timecode)

        minute = int(number.group(1) or 0)
        seconde = int(number.group(2) or 0)
        
        temps = 60*minute+seconde
    elif ':' in timecode:
        number = re.search(r'(?:(\d+):)?(?:(\d+))?',timecode)

        minute = int(number.group(1) or 0)
        seconde = int(number.group(2) or 0)
        
        print(minute,seconde)
        temps = 60*minute+seconde
    else:
        
        temps = int(timecode) 
        seconde = temps%60
        minute = int((temps-seconde)/60)
    bot.vc.stop()

    bot.vc.play(discord.FFmpegPCMAudio(
        f"Music/Youtube/{bot.current_music}",
        options=f"-ss {temps}"
    ))
    bot.isGoto=False

    
    seconde_str = '0' + str(seconde) if seconde < 10 else seconde 
    minute_str = '0' + str(minute) if minute < 10 else minute
    await interaction.response.send_message(f"Avancement vers {minute_str}:{seconde_str}",ephemeral=True)

@bot.tree.command(name="queue",description=message.fgoto,guild=GUILD_ID)
async def queue(interaction: discord.Interaction): 
    temp_file=deepcopy(MUSIC_FILE)
    embed = discord.Embed(title="Music queue",description="The list of music") 
    while(not temp_file.est_vide()):
        music = temp_file.defiler()
        music_name = music.split('@')[1].replace("mp3","")
        embed.add_field(name=f"{music_name}", value=" ")

    await interaction.response.send_message(embed=embed)



bot.run(get_token())

