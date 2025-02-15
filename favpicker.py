import songs
import picker
import spotify
import streamlit as st
import pandas as pd

#initialize global variables
if 'songlist' not in st.session_state:
    st.session_state.songlist = []
    st.session_state.favsong = []
    st.session_state.total = 0
    st.session_state.l = 0 #index for buttons
    st.session_state.i = 0 #index for selecting what songs to show
    st.session_state.goodlink = False
    st.session_state.currentfav = ""


currentfav = ""
keepGoing = True
favcount = 0

def get_songs(playlist):
    global total
    for track in playlist:
        this_song = songs.Song(track)
        st.session_state.songlist.append(this_song)
        st.session_state.total += 1   

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
    
   
#add the new favorite song to the list and remove it from the original
def newFave():
    for song in st.session_state.songlist:
        if song.eliminated == False:
            st.session_state.favsong.append(song)
            st.session_state.songlist.remove(song)
            st.session_state.currentfav = song
    # for song in songlist:
    #         print(song.name)
    
#check if only one song is remaining
def isFinished():
    count = 0
    for song in st.session_state.songlist:
        if song.eliminated == False:
            count += 1
    if count > 1:
        return False
    else: 
        return True
    
def handle_choice(winner, loser, i):
    loser.elim(winner)
    # picking(i)
    # st.rerun()

    
def picking(i):
    if isFinished() == False:

        #pick the two choices that the user will choose from by iterating through the list
        j = i
        choice1 = choicepicker(st.session_state.songlist,i)
        #if rest of the songs have been eliminated go through list from the beginning
        if choice1 == None: 
            i = 0
            choice1 = choicepicker(st.session_state.songlist,i)
        i = st.session_state.songlist.index(choice1) + 1
        choice2 = choicepicker(st.session_state.songlist,i)
        if choice2 == None:
            i = 0
            choice2 = choicepicker(st.session_state.songlist,i)
        i = st.session_state.songlist.index(choice2) + 1


        st.write("Pick your favorite")
        st.button(
            label = choice1.song_str,
            key=f"choice1_{i}",
            on_click=lambda: handle_choice(choice1, choice2, i)
        )
        st.button(
            label = choice2.song_str,
            key=f"choice2_{i}",
            on_click=lambda: handle_choice(choice2, choice1, i)
        )        

def we_keep_going():
    st.rerun()

def end_of_game():
    s = ""
    count = 1
    st.write("All Done!")
    #add the last song to the list after choosing ends
    if keepGoing != False:
        for song in st.session_state.songlist: st.session_state.favsong.append(song)
    for song in st.session_state.favsong:
        s += f"{count}. {song.song_str}\n"
        count += 1
    st.write("Your favorites are: ")
    st.write(s)

    

def link_entered(link):
    playlist_link = st.session_state.Link
    if len(playlist_link) == 76:
        playlist_id = playlist_link[34:56]
        playlist = spotify.search_playlist(token, playlist_id)
        if playlist != None:
            st.session_state.goodlink = True
            get_songs(playlist)
            st.rerun()
            # picker.start_picking(playlist)
            # favsong = picker.picking(songlist)
        else:
            st.write("Invalid Link. Please make sure the playlist is public and not empty.")
    else:
        st.write("Invalid Link. Please make sure the playlist is public and not empty.")


token = spotify.get_token()

   

st.title("Favorite Song Picker")
if st.session_state.goodlink == False:
    link = st.text_input("Please enter in the spotify link for your playlist. Please make sure the playlist is public!",
                     key = "Link",
                    #  on_change =lambda: link_entered(link)
                     )
    if link != "":
        link_entered(link)

else:
    favcount = len(st.session_state.favsong)
    currenttotal = len(st.session_state.songlist)

    s = ""
    i = 0

    #check if there is only one song remaining and skip the choosing 
    if favcount < st.session_state.total - 1:
        if favcount != 0:
            #make it so songs that were eliminated by last favorite are now marked as not eliminated
            for song in st.session_state.songlist:
                if song.eliminator == st.session_state.currentfav:
                    song.eliminated = False
                    # newlist.append(song)

        # picking(0)

        if isFinished() == False:

            # ensure that even if last 2 choices are properly asked even if they haven't been eliminated by the same song
            if currenttotal < 3:
                for song in st.session_state.songlist:
                    song.eliminated = False 

            #pick the two choices that the user will choose from by iterating through the list
            choice1 = choicepicker(st.session_state.songlist,i)
            #if rest of the songs have been eliminated go through list from the beginning
            if choice1 == None: 
                i = 0
                choice1 = choicepicker(st.session_state.songlist,i)
            i = st.session_state.songlist.index(choice1) + 1
            choice2 = choicepicker(st.session_state.songlist,i)
            if choice2 == None:
                i = 0
                choice2 = choicepicker(st.session_state.songlist,i)
            i = st.session_state.songlist.index(choice2) + 1


            st.write("Pick your favorite")
            st.button(
                label = choice1.song_str,
                key=f"choice1_{st.session_state.l}",
                on_click=lambda: handle_choice(choice1, choice2, i)
            )
            st.button(
                label = choice2.song_str,
                key=f"choice2_{st.session_state.l+1}",
                on_click=lambda: handle_choice(choice2, choice1, i)
            )        
            st.session_state.l += 1
            # for song in st.session_state.songlist:
                # print(song.song_str)
                # print('-------------------------')

        else:
            newFave()
            if len(st.session_state.songlist) == 1:
                st.rerun()
            count =1
            for song in st.session_state.favsong:
                s += f"{count}. {song.song_str}\n"
                count += 1
            st.write("Your favorites are:")
            st.write(s)

            st.write("Would you like to keep going?")
            st.button(
                label = "Yes",
                key="yes",
                # on_click=lambda: we_keep_going()
            )
            keepGoing = st.button(
                label = "No",
                key="no",
                on_click=lambda:exit
            )
    else: end_of_game()


