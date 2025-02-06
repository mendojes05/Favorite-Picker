class Song:

    def __init__(self, track):
        self.track = track
        self.name = track["track"]["name"]
        self.artists = track['track']['artists'][0]['name']

        #check if there are any other artists of the song
        for artists in track['track']['artists'][1:]:
            self.artists = f"{self.artists}, {artists['name']}"
        self.song_str = f"{self.name} - {self.artists}"
        self.eliminated = False


    #method to set when eliminated
    def elim(self, Song):
        self.eliminated = True
        self.eliminator = Song

    def printOut(self):
        print("The song title is "+ self.name)