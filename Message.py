class Message:
    def __init__(self):
        self.welcome = "🌴 Coconuts Vibes V2, by BerretMan"

        self.joinChannel = "Joined the voice channel." 
        self.leaveChannel = "Left the voice channel."
        self.noChannel = "⚠️ ERROR ⚠️: You are not in a voice channel."
        self.downloading = "Downloading... please wait."
        self.download = "Download complete!"
        
        self.noMusic = "The playlist is currently empty."

        self.pause = "Music paused."
        self.play = "Music resumed."

        self.x1 = "Playback speed set to 1x."
        self.x2 = "Playback speed set to 2x."

        # Slash Command description
        self.fjoin = "CoconutsVibes joins the voice channel"
        self.fleave = "CoconutsVibes leaves the voice channel"
        self.fadd = "Add a song to the playlist" 
        self.fstart = "Start playing songs from the CoconutsVibes playlist"
        self.fgoto = "Jump to a specific timestamp in the song"
        self.fqueue = "Show the current playlist"

    def next(self, music_name):
        return f"Now playing: **{music_name}**!"
