import songs
import picker
import spotify
colors = [
    "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink", "Brown",
    "Black", "White"
]

#initialize variables
songlist = []
favsong = []
favcount = 0

print("Please enter in the spotify link for your playlist. Please make sure the playlist is public!")
playlist_link = input()
playlist_id = playlist_link[34:56]
# print(playlist_id)

token = spotify.get_token()
playlist = spotify.search_playlist(token, playlist_id)
# # for song in playlist:
# #     print(song["track"]["name"])
for track in playlist:
    # this_song = songs.Song(track["track"]["name"], track['track']['artists'][0]['name'])
    this_song = songs.Song(track)
    songlist.append(this_song)
    # list.append(newSong)




#first round of picking
total = len(songlist)

i  = 0
while picker.isFinished(songlist) == False:
    
    #pick the two choices that the user will choose from by iterating through the list
    choice1 = picker.choicepicker(songlist,i)
    # if reached the end of the list go back to the beginning
    if choice1 == None: 
        i = 0
        continue
    i = songlist.index(choice1) + 1
    choice2 = picker.choicepicker(songlist,i)
    if choice2 == None:
        i = 0
        choice2 = picker.choicepicker(songlist,i)
    i = songlist.index(choice2) + 1

    print("Pick your favorite")
    # print(f"(1) {choice1.name} - {choice1.artist} \n(2) {choice2.name} - {choice2.artist}")
    print(f"(1) {choice1.song_str} \n(2) {choice2.song_str}")

    ans = input()
    if ans == "1":
        choice2.elim(choice1)
    elif ans == "2":
        choice1.elim(choice2)

picker.newFave(songlist,favsong)
print("Your favorite is " + favsong[0].song_str)
print()
currentfav = favsong[0]

#keep going to picke the second fav and so on
#todo: ask if they want to continue and add edge cases
# remaining_songs = songlist
while len(favsong) < total - 1:
    print("Would you like to keep going? y/n")
    keepGoing = input()
    print()
    if keepGoing == "n": break
    i = 0
    newlist = []
    for song in songlist:
        if song.eliminator == currentfav:
            song.eliminated = False
            # newlist.append(song)
    newtotal = len(songlist)
    # print("New total is " + str(newtotal))
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
        i = songlist.index(choice2) + 1

        print("Pick your favorite")
        print(f"(1) {choice1.song_str} \n(2) {choice2.song_str}")
        # print("(1) " + choice1.name + " (2) " + choice2.name)

        ans = input()
        if ans == "1":
            choice2.elim(choice1)
        elif ans == "2":
            choice1.elim(choice2)

    picker.newFave(songlist,favsong)
    favcount += 1
    print("Your favorites are: ")
    for idx, song in enumerate(favsong):
        print(f"{idx + 1}. {song.song_str}")
    print()
    currentfav = favsong[favcount]
    # songlist.remove(currentfav)


if ans == "1":
    favsong.append(choice2)
elif ans == "2":
    favsong.append(choice1)
print("All Done!")
print("Your favorites are: ")
for idx, song in enumerate(favsong):
    print(f"{idx + 1}. {song.song_str}")