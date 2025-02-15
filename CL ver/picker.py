import songs

#pick a song that hasn't been eliminated
def choicepicker(songlist, i):
    #check if we've reached the end of the list of songs and return None
    if i == len(songlist):
        return None    
    elif songlist[i].eliminated == False:
        return songlist[i]
    #if the song has been eliminated check the next one in the list
    else:
        return choicepicker(songlist,i+1)
    
# def newchoicepicker(remaining_songs,i):
    #check if we've reached the end of the list of songs and return None
    if i == len(remaining_songs):
        return None    
    elif remaining_songs[i].eliminated == False and remaining_songs[i]:
        return newlist[i]
    #if the song has been eliminated check the next one in the list
    else:
        return newchoicepicker(i+1)
    
#add the new favorite song to the list and remove it from the original
def newFave(songlist,favsong):
    for song in songlist:
        if song.eliminated == False:
            favsong.append(song)
            songlist.remove(song)
    print("**********")
    for song in songlist:
            print(song.name)
    print("**********")    

# def newnewFave():
#     for song in newlist:
#         if song.eliminated == False:
#             favsong.append(song)
#             songlist.remove(songlist.index(song.name))
    
#check if only one song is remaining
def isFinished(songlist):
    count = 0
    for song in songlist:
        if song.eliminated == False:
            count += 1
    if count > 1:
        return False
    else: 
        return True
    
# def newisFinished():
#     count = 0
#     for song in newlist:
#         if song.eliminated == False:
#             count += 1
#     if count > 1:
#         return False
#     else: 
#         newFave()
#         return True