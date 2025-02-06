import songs
import picker
import spotify

#initialize variables
songlist = []
favsong = []
favcount = 0
goodlink = False

token = spotify.get_token()

print("Please enter in the spotify link for your playlist. Please make sure the playlist is public!")

while goodlink == False:
    playlist_link = input()
    if len(playlist_link) == 76:
        playlist_id = playlist_link[34:56]
        playlist = spotify.search_playlist(token, playlist_id)
        if playlist != None:
            break
    print("Invalid Link. Please make sure the playlist is public and not empty.\nEnter new link:")



for track in playlist:
    this_song = songs.Song(track)
    songlist.append(this_song)
    # list.append(newSong)




total = len(songlist)

i  = 0
while len(favsong) < total - 1:
    i = 0
    #don't show continue message if in first round
    if len(favsong) != 0:
        print("Would you like to keep going?\n(1) Yes\n(2) No")
        keepGoing = input()
        print()
        if keepGoing == "2": break
        elif keepGoing != "1": print("Please enter 1 or 2"); continue # make sure user entered 1 or 2
        #make it so songs that were eliminated by last favorite are now marked as not eliminated
        for song in songlist:
            if song.eliminator == currentfav:
                song.eliminated = False
                # newlist.append(song)
        newtotal = len(songlist)
        # ensure that even if last 2 choices are properly asked even if they haven't been eliminated by the same song
        if newtotal < 3:
            for song in songlist:
                song.eliminated = False

        
    while picker.isFinished(songlist) == False:

    #pick the two choices that the user will choose from by iterating through the list
        choice1 = picker.choicepicker(songlist,i)
        if choice1 == None: 
            i = 0
            continue
        i = songlist.index(choice1) + 1
        choice2 = picker.choicepicker(songlist,i)
        if choice2 == None:
            i = 0
            choice2 = picker.choicepicker(songlist,i)

        print("Pick your favorite")
        print(f"(1) {choice1.song_str} \n(2) {choice2.song_str}")
        # print("(1) " + choice1.name + " (2) " + choice2.name)

        ans = input()
        if ans == "1":
            choice2.elim(choice1)
        elif ans == "2":
            choice1.elim(choice2)
        else: 
            print("Please enter 1 or 2")
            continue
        
        i = songlist.index(choice2) + 1
    

    picker.newFave(songlist,favsong)
    favcount += 1
    print("Your favorites are: ")
    for idx, song in enumerate(favsong):
        print(f"{idx + 1}. {song.song_str}")
    print()
    currentfav = favsong[favcount-1]
    # songlist.remove(currentfav)

#add the last song to the list after choosing ends
if keepGoing != "2":
    if ans == "1":
        favsong.append(choice2)
    elif ans == "2":
        favsong.append(choice1)
print("All Done!")
print("Your favorites are: ")
for idx, song in enumerate(favsong):
    print(f"{idx + 1}. {song.song_str}")