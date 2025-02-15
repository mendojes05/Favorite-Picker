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
    st.session_state.state = 0
    st.session_state.currentfav = ""
    st.session_state.playlist_name = ""
    st.session_state.platylist_cover = ""


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
    show_favs()

def show_favs():
    count = 1
    st.write("Your favorites are:")
    s=""
    for song in st.session_state.favsong:
        listcont = st.container(border=True,height=200)
        listcol = listcont.columns([0.1,0.6,0.3])

        listcol[0].write("")
        listcol[0].write("")
        listcol[0].write("")
        listcol[0].markdown(f"**{count})**")

        listcol[2].image(image=song.cover,width=165)
        
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].markdown(f"**{song.name}**")
        listcol[1].markdown(f"{song.artists}")
        count += 1    

def show_playlist():
    count = 1
    st.markdown(f"You chose playlist:")
    playlistcol = st.columns(3)
    playlistcol[1].image(image=st.session_state.playlist_cover)
    # playlistcol2 = playlistcol[1].columns([0.2,0.6,0.2])
    # playlistcol[1].markdown(f"**{st.session_state.playlist_name}**")
    playlistcol[1].markdown(
    f"""
    <div style="text-align: center; font-weight: bold; font-size: 18px;">
        {st.session_state.playlist_name}
    </div>
    """,
    unsafe_allow_html=True
    )
    # playlistcol[1].markdown(<div style="text-align: center"> {st.session_state.playlist_name} </div>)
    for song in st.session_state.songlist:
        listcont = st.container(border=True,height=200)
        listcol = listcont.columns([0.1,0.6,0.3])

        listcol[0].write("")
        listcol[0].write("")
        listcol[0].write("")
        listcol[0].markdown(f"**{count})**")

        listcol[2].image(image=song.cover,width=165)
        
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].markdown(f"**{song.name}**")
        listcol[1].markdown(f"{song.artists}")
        count += 1    
        
  

def link_entered(link):
    playlist_link = link
    if len(playlist_link) == 76:
        playlist_id = playlist_link[34:56]
        playlist = spotify.search_playlist(token, playlist_id)
        playlist_tracks = playlist["tracks"]["items"]
        st.session_state.playlist_name = playlist['name']
        st.session_state.playlist_cover = playlist['images'][0]['url']
        if playlist != None:
            st.session_state.state = 1
            get_songs(playlist_tracks)
            st.rerun()
        else:
            st.write("Invalid Link. Please make sure the playlist is public and not empty.")
    else:
        st.write("Invalid Link. Please make sure the playlist is public and not empty.")

def change_playlist():
    st.session_state.songlist = []
    st.session_state.Link = ""
    st.session_state.state = 0

def start_picking():
    st.session_state.state = 2

token = spotify.get_token()


st.title("Find out your favorite song")
if st.session_state.state == 0:
    link = st.text_input("Please enter in the spotify link for your playlist. Please make sure the playlist is public!",
                     key = "Link",
                    #  on_change =lambda: link_entered(link)
                     )
    if link != "":
        link_entered(link)

elif st.session_state.state == 1:
    show_playlist()
    startcol = st.columns(3)
    startcol[1].write("Would you like to start picking?")

    start = startcol[1].columns(2)
    start[0].button(
        label = "Start Picking",
        key="start",
        on_click=lambda:start_picking()
    )
    keepGoing = start[1].button(
        label = "Change Playlist",
        key="change",
        on_click=lambda:change_playlist()
    )    

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
            cont1 = col[0].container(
                border=True,
                height=500
            )
            cont1.image(
                image=choice1.cover
            )
            cont1.markdown(f"**{choice1.name}**")
            cont1.markdown(choice1.artists)
            cont1col = cont1.columns([0.75,0.25])
            cont1col[0].button(
                label = "Select",
                key=f"choice1_{st.session_state.l}",
                on_click=lambda: handle_choice(choice1, choice2)
            )
            cont1col[1].link_button(
                label="Listen",
                url=choice1.link
            )


            cont2 = col[1].container(
                border=True,
                height=500
            )
            cont2.image(
                image=choice2.cover
            )
            cont2.markdown(f"**{choice2.name}**")
            cont2.markdown(choice2.artists)
            cont2col = cont2.columns([0.75,0.25])
            cont2col[0].button(
                label = "Select",
                key=f"choice2_{st.session_state.l+1}",
                on_click=lambda: handle_choice(choice2, choice1)
            )        
            cont2col[1].link_button(
                label="Listen",
                url=choice2.link
            )            
            st.session_state.l += 1


        else:
            newFave()

            #check if there is only one song left and rerun if there is
            if len(st.session_state.songlist) == 1:
                st.rerun()

            #make it so songs that were eliminated by last favorite are now marked as not eliminated
            songcount = 0
            thissong = "" #placeholder for current song when iterating
            for song in st.session_state.songlist:
                if song.eliminator == st.session_state.currentfav:
                    song.eliminated = False
                    thissong = song
                    songcount += 1
            #checks if there is only one song that was eliminated by the current fav            
            if songcount < 2:
                st.rerun()


            # # ensure that even if last 2 choices are properly asked even if they haven't been eliminated by the same song
            # if len(st.session_state.songlist) < 3:
            #     if st.session_state.songlist[0].eliminator == st.session_state.songlist[1]:
            #     for song in st.session_state.songlist:
            #         song.eliminated = False

            st.session_state.i = 0
            show_favs()

            keepgoingcol = st.columns(3)
            keepgoingcol[1].write("Would you like to keep going?")

            yesno = keepgoingcol[1].columns(2)
            yesno[0].button(
                label = "Yes",
                key="yes",
            )
            keepGoing = yesno[1].button(
                label = "No",
                key="no",
                on_click=lambda:end_of_game()
            )
    else: end_of_game()


