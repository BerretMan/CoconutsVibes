import discord
from discord.ext import commands
from Message import Message
class Button(discord.ui.View):
    def __init__(self, bot, playlist):
        super().__init__(timeout=None)
        self.bot = bot
        self.playlist = playlist
        self.music=bot.current_music
        self.vc = bot.vc
        self.is_2 = False
        self.message = Message()

    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.primary)
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.vc:
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
            self.bot.isGoto = True
            self.vc.stop()

            self.is_2 = not self.is_2
            options = "-filter:a atempo=2.0" if self.is_2 else ""
            msg = self.message.x2 if self.is_2 else self.message.x1
            self.vc.play(discord.FFmpegPCMAudio(
                source=f"Music/Youtube/{self.bot.current_music}",
                options=options
            ))

            self.bot.isGoto = False
            await interaction.response.send_message(msg,ephemeral=True)

    @discord.ui.button(label="⏭️",style=discord.ButtonStyle.secondary)
    async def next(self,interaction: discord.Interaction, button: discord.ui.Button):
        if not self.vc:
            return

        if self.playlist.est_vide():
            await interaction.response.send_message(self.message.noMusic, ephemeral=True)
            return

        self.vc.stop()
        await interaction.response.send_message("Musique suivante",ephemeral=True)
