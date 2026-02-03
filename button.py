import discord
from discord.ext import commands
from Message import Message
class Button(discord.ui.View):
    def __init__(self, vc, playlist,music):
        super().__init__(timeout=None)  
        self.vc = vc
        self.playlist = playlist
        self.music=music
        self.is_2 = False 
        self.message = Message()

    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.primary)
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.vc:
            await interaction.response.send_message(self.message.noChannel, ephemeral=True)
            return

        if self.vc.is_paused():
            self.vc.resume()
            await interaction.response.send_message(self.message.play, ephemeral=True)

        elif self.vc.is_playing():
            self.vc.pause()
            await interaction.response.send_message(self.message.pause, ephemeral=True)
   
    @discord.ui.button(label="x2",style=discord.ButtonStyle.success)
    async def speed2(self,interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc and self.vc.is_playing():
            self.vc.stop()

            print(self.music) 
            if self.is_2:
                self.vc.play(discord.FFmpegPCMAudio(source=f"Music/Youtube/{self.music}"))
                
                self.is_2 = not self.is_2
                await interaction.response.send_message(self.message.x1, ephemeral=True)
            else:
                self.vc.play(discord.FFmpegPCMAudio(source=f"Music/Youtube/{self.music}",options=f"-filter:a"))
                self.is_2 = not self.is_2
                await interaction.response.send_message(self.message.x2, ephemeral=True)
                

    @discord.ui.button(label="⏭️",style=discord.ButtonStyle.secondary)
    async def next(self,interaction: discord.Integration, button: discord.ui.Button):
        if not self.vc:
            await interaction.response.send_message(self.message.noChannel, ephemeral=True)
            return

        self.vc.pause()
        if not self.playlist.est_vide():
            self.music= self.playlist.defiler()
        self.vc.play(discord.FFmpegPCMAudio(source=f"Music/Youtube/{self.music}",options="-filter:a atempo=2.0"))

        music_name = self.music.split('@')[1].replace(".mp3","")
        await interaction.response.send_message(self.message.next(music_name), ephemeral=True)
