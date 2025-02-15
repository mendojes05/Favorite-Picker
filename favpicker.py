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
st.set_page_config(
    page_title="Fav Song Picker",
    layout="centered"
)

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
    
def handle_choice(winner, loser):
    loser.elim(winner)   

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
    i = st.session_state.i

    #check if there is only one song remaining and skip the choosing 
    if len(st.session_state.songlist) > 1:

        if isFinished() == False:

            #pick the two choices that the user will choose from by iterating through the list
            choice1 = choicepicker(st.session_state.songlist,st.session_state.i)
            #if rest of the songs have been eliminated go through list from the beginning
            if choice1 == None: 
                st.session_state.i = 0
                choice1 = choicepicker(st.session_state.songlist,st.session_state.i)
            st.session_state.i = st.session_state.songlist.index(choice1) + 1
            choice2 = choicepicker(st.session_state.songlist,st.session_state.i)
            if choice2 == None:
                st.session_state.i = 0
                choice2 = choicepicker(st.session_state.songlist,st.session_state.i)
            st.session_state.i = st.session_state.songlist.index(choice2) + 1


            st.write("Pick your favorite")
            col = st.columns(2)
            col[0].button(
                label = choice1.song_str,
                key=f"choice1_{st.session_state.l}",
                on_click=lambda: handle_choice(choice1, choice2)
            )
            col[1].button(
                label = choice2.song_str,
                key=f"choice2_{st.session_state.l+1}",
                on_click=lambda: handle_choice(choice2, choice1)
            )        
            st.session_state.l += 1


        else:
            newFave()

            #check if there is only one song left and rerun if there is
            if len(st.session_state.songlist) == 1:
                st.rerun()

            #make it so songs that were eliminated by last favorite are now marked as not eliminated
            for song in st.session_state.songlist:
                if song.eliminator == st.session_state.currentfav:
                    song.eliminated = False

            # ensure that even if last 2 choices are properly asked even if they haven't been eliminated by the same song
            if len(st.session_state.songlist) < 3:
                for song in st.session_state.songlist:
                    song.eliminated = False

            st.session_state.i = 0
            count = 1
            for song in st.session_state.favsong:
                s += f"{count}. {song.song_str}\n"
                count += 1
            st.write("Your favorites are:")
            st.write(s)

            st.write("Would you like to keep going?")
            st.button(
                label = "Yes",
                key="yes",
            )
            keepGoing = st.button(
                label = "No",
                key="no",
                on_click=lambda:end_of_game()
            )
    else: end_of_game()


