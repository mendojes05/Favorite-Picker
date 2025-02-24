import songs
import streamlit as st
import random
import tekore as tk
import os


#initialize global variables and other intilization tasks
if 'songlist' not in st.session_state:
    st.session_state.songlist = []
    st.session_state.favsong = []
    st.session_state.total = 0
    st.session_state.l = 0 #index for buttons
    st.session_state.i = 0 #index for selecting what songs to show
    st.session_state.state = 0
    st.session_state.currentfav = ""
    st.session_state.list_name = ""
    st.session_state.platylist_cover = ""
    st.session_state.elim_countdown = 0
    st.session_state.song_ids = set()
    st.session_state.song_names = set()


st.set_page_config(
    page_title="Fav Song Picker",
    layout="wide"
)

def get_token():
    app_token = tk.request_client_token(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
    spotify = tk.Spotify(app_token)
    return spotify

def get_playlist_songs(alltracks):
    for track in alltracks:
        song_id = track.track.id
        #make sure the song isn't already in the list
        if song_id not in st.session_state.song_ids:
            st.session_state.song_ids.add(song_id)
            this_song = songs.Song(track.track)
            st.session_state.songlist.append(this_song)
            st.session_state.total += 1   
        #check through the song names if the current track is local
        elif song_id == None:
            duplicate = False
            for song in st.session_state.songlist:
                if song.name == track.track.name:
                    duplicate = True
                    break
            if duplicate == False:
                this_song = songs.Song(track.track)
                st.session_state.songlist.append(this_song)
                st.session_state.total += 1

def get_album_songs(album):
    for track in album:
        full_track = spotify.track(track.id)
        #make sure the song isn't already in the list
        if track.name not in st.session_state.song_names:
            st.session_state.song_names.add(track.name)
            this_song = songs.Song(full_track)
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
    st.session_state.elim_countdown += -1   

def end_of_game(normal_end):
    endcol = st.columns(3)
    endcol[1].markdown(
    f"""
    <div style="text-align: center; font-size: 26px;">
        All Done!
    </div>
    """,
    unsafe_allow_html=True
    )     #add the last song to the list after choosing ends
    if normal_end == True:
        for song in st.session_state.songlist: st.session_state.favsong.append(song)
    show_favs()

def stop_picking():
    st.session_state.songlist = []

def show_favs():
    count = 1
    favcol = st.columns(3)
    favcol[1].markdown(
    f"""
    <div style="text-align: center; font-size: 18px;">
        Your favorites are:
    </div>
    """,
    unsafe_allow_html=True
    )
    playlistcol = st.columns([0.25,0.75,0.25])
    s=""
    for song in st.session_state.favsong:
        listcont = playlistcol[1].container(border=True,height=250)
        listcol = listcont.columns([0.1,0.6,0.3])

        listcol[0].write("")
        listcol[0].write("")
        listcol[0].write("")
        if count == 1:
            listcol[0].header(''':first_place_medal:''')
        elif count == 2:
            listcol[0].header(''':second_place_medal:''')
        elif count == 3:
            listcol[0].header(''':third_place_medal:''')
        else:
            listcol[0].header(count)


        listcol[2].image(image=song.cover,width=215)
        
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].subheader(f"**{song.name}**")
        listcol[1].markdown(f"{song.artists}")
        count += 1    

def show_playlist():
    count = 1
    covercol = st.columns(3)
    playlistcol = st.columns([0.25,0.75,0.25])
    covercol[1].markdown(
    f"""
    <div style="text-align: center; font-size: 18px;">
        You chose these songs:
    </div>
    """,
    unsafe_allow_html=True
    )    
    # covercol[1].image(image=st.session_state.list_cover,width=300)
    covercol[1].markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="{st.session_state.list_cover}" width="300">
    </div>
    """,
    unsafe_allow_html=True
)
    # playlistcol2 = playlistcol[1].columns([0.2,0.6,0.2])
    # playlistcol[1].markdown(f"**{st.session_state.list_name}**")
    playlistcol[1].markdown(
    f"""
    <div style="text-align: center; font-weight: bold; font-size: 18px;">
        {st.session_state.list_name}
    </div>
    """,
    unsafe_allow_html=True
    )
    # playlistcol[1].markdown(<div style="text-align: center"> {st.session_state.list_name} </div>)
    for song in st.session_state.songlist:
        listcont = playlistcol[1].container(border=True,height=250)
        listcol = listcont.columns([0.1,0.6,0.3])

        listcol[0].write("")
        listcol[0].write("")
        listcol[0].write("")
        listcol[0].header(count)

        listcol[2].image(image=song.cover,width=215)
        
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].subheader(f"**{song.name}**")
        listcol[1].markdown(f"{song.artists}")
        count += 1    
        
  

def link_entered(link):
    #user entered playlist link
    if len(link) == 76:
        playlist_id = link[34:56]
        playlist = spotify.playlist(playlist_id)
        if playlist != None:
            st.session_state.list_name = playlist.name
            st.session_state.list_cover = spotify.playlist_cover_image(playlist_id)[0].url
            alltracks = spotify.all_items(spotify.playlist_items(playlist_id)) #bypass the limit of 100 songs and add all
            st.session_state.state = 1
            get_playlist_songs(alltracks)
            st.rerun()
        else:
            linkcol[1].write("Invalid Link. Please make sure the playlist is public and not empty.")
    #user entered album link
    elif len(link) == 79:
        album_id = link[31:53]
        album = spotify.album(album_id)
        if album != None:
            st.session_state.list_name = album.name
            st.session_state.list_cover = album.images[0].url
            st.session_state.state = 1
            alltracks = album.tracks.items
            get_album_songs(alltracks)
            st.rerun()
    #user ewntered artist link
    elif len(link) == 80:
        artist_id = link[32:54]
        artist = spotify.artist(artist_id)
        albums = spotify.artist_albums(artist_id).items
        if artist != None:
            st.session_state.list_name = artist.name
            st.session_state.list_cover = artist.images[0].url
            st.session_state.state = 1
            for album in albums:
                this_album = spotify.album(album.id)
                alltracks = this_album.tracks.items
                get_album_songs(alltracks)
            st.rerun()
    else:
        linkcol[1].write("Invalid Link. Please make sure the playlist is public and not empty.")

def change_playlist():
    st.session_state.songlist = []
    st.session_state.Link = ""
    st.session_state.state = 0

def start_picking():
    st.session_state.state = 2
    random.shuffle(st.session_state.songlist)

spotify = get_token()

pagecol = st.columns([0.25,0.75,0.25])
# pagecol[1].title(''':musical_note: Find out your favorite song :musical_note:''')
pagecol[1].markdown(
    """
    <h1 style="text-align: center;">🎵 Find out your favorite song 🎵</h1>
    """,
    unsafe_allow_html=True
)

linkcol = st.columns([0.40,0.5,0.40])

if st.session_state.state == 0:
    link = linkcol[1].text_input("Please enter in the spotify link for your playlist, artist or album. Please make sure the playlist is public!",
                     key = "Link",
                    #  on_change =lambda: link_entered(link)
                     )
    if link != "":
        link_entered(link)

elif st.session_state.state == 1:
    st.session_state.elim_countdown = len(st.session_state.songlist) - 1
    startcol = st.columns(3)
    startcol[1].markdown(
    f"""
    <div style="text-align: center; font-size: 18px;">
        Would you like to start picking?
    </div>
    """,
    unsafe_allow_html=True
    )     

    start = startcol[1].columns([0.2,0.1,0.1,0.2])
    start[1].button(
        label = "Start Picking",
        key="start",
        on_click=lambda:start_picking()
    )
    keepGoing = start[2].button(
        label = "Change Playlist",
        key="change",
        on_click=lambda:change_playlist()
    )    
    show_playlist()

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



            col = st.columns([0.1,0.1,0.1,0.1])
            pick_container = col[1].container(
                height=50,
                border=False
            )
            pick_container.subheader("Pick your favorite")
            pick_container2 = col[2].container(
                height=50,
                border=False
            )
            pick_container3 = col[3].container(
                height=50,
                border=False
            )
            countdown_container = col[3].container(
                height=580,
                border=False
            )
            countdown_container.markdown(
                f"""
                <div style="
                    position: relative; 
                    width: 100%; 
                    height: 580px; 
                    display: flex; 
                    flex-direction: column;
                    justify-content: center; 
                    align-items: center; 
                    text-align: center;
                    font-size: 26px; /* Adjust as needed */
                    line-height: 1.2;
                ">
                    <span style="font-size: 72px; font-weight: bold;line-height: 0.5;">
                        {st.session_state.elim_countdown}
                    </span>
                    <br>
                    more eliminations until
                    <br>
                    next favorite is found
                </div>
                """,
                unsafe_allow_html=True
            )       



            cont1 = col[1].container(
                border=True,
                height=580
            )
            cont1.image(
                image=choice1.cover,
                use_container_width=True
            )
            cont1.markdown(f"**{choice1.name}**")
            cont1.markdown(choice1.artists)
            cont1col = cont1.columns([0.75,0.25])
            cont1col[0].button(
                label = "Select",
                key=f"choice1_{st.session_state.l}",
                on_click=lambda: handle_choice(choice1, choice2)
            )
            if choice1.link != None:
                cont1col[1].link_button(
                    label="Listen",
                    url=choice1.link
                )


            cont2 = col[2].container(
                border=True,
                height=580
            )
            cont2.image(
                image=choice2.cover,
                use_container_width=True
            )
            cont2.markdown(f"**{choice2.name}**")
            cont2.markdown(choice2.artists)
            cont2col = cont2.columns([0.75,0.25])
            cont2col[0].button(
                label = "Select",
                key=f"choice2_{st.session_state.l+1}",
                on_click=lambda: handle_choice(choice2, choice1)
            )
            if choice2.link != None:         
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
            st.session_state.elim_countdown = songcount - 1 #set countdown to how many songs are to be shown next 


            # # ensure that even if last 2 choices are properly asked even if they haven't been eliminated by the same song
            # if len(st.session_state.songlist) < 3:
            #     if st.session_state.songlist[0].eliminator == st.session_state.songlist[1]:
            #     for song in st.session_state.songlist:
            #         song.eliminated = False

            #reset choice index and elim countdown
            st.session_state.i = 0
            show_favs()

            keepgoingcol = st.columns(3)
            # keepgoingcol[1].write("Would you like to keep going?")
            keepgoingcol[1].markdown(
            f"""
            <div style="text-align: center; font-size: 18px;">
                Would you like to keep going?
            </div>
            """,
            unsafe_allow_html=True
            )

            yesno = keepgoingcol[1].columns([0.2,0.1,0.1,0.2])
            yesno[1].button(
                label = "Yes",
                key="yes",
            )
            keepGoing = yesno[2].button(
                label = "No",
                key="no",
                on_click=lambda:stop_picking()
            )
    elif len(st.session_state.songlist) == 1: end_of_game(True)
    else: end_of_game(False)