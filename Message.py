class Message:
    def __init__(self):
        self.welcome = f"🌴Coconuts Vibes V2, by BerretMan"

        self.joinChannel  ="Channel rejoint." 
        self.leaveChannel ="Channel quitté."
        self.noChannel = "⚠️ERREUR⚠️: vous n'êtes dans aucun channel."
        self.downloading = "Téléchargment en cours... "
        self.download = "Le téléchargement est terminé"
        
        self.noMusic = "Il n'y a pas de musique dans la playlist."

        self.pause = "La musique est en pause."
        self.play = "La musique reprends."

        self.x1 = " La musique est joué en x1."
        self.x2 = " La musique est joué en x2."

        #commande 
        self.fjoin = "CoconutsVibes rejoint le channel"
        self.fleave = "CoconutsVibes quitte le channel"
        self.fadd = "Ajoute une musique dans la playlist" 
        self.fstart = "Lance les musiques contenus dans la playlist de CoconutsVibes"
        self.fgoto = "Avance la musique au timecode souhaité"
        self.fqueue = "Affiche la playlist"

    
    def next(self,music_name):
        return f"{music_name} est maintenant joué!"
