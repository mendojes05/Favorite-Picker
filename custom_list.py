import songs
import streamlit as st
import random
import items
import os

#initialize global variables and other intilization tasks
if 'list' not in st.session_state:
    st.session_state.list = []
    st.session_state.favs = []
    st.session_state.total = 0
    st.session_state.l = 0 #index for buttons
    st.session_state.i = 0 #index for selecting what songs to show
    st.session_state.state = 0
    st.session_state.currentfav = ""
    st.session_state.list_name = ""
    st.session_state.elim_countdown = 0
    st.session_state.prev_choices = []
    st.session_state.prev_choiceL = ""

st.set_page_config(
    page_title="Fav Picker",
    layout="wide"
)

#pick a song that hasn't been eliminated
def choicepicker(list, i):
    #check if we've reached the end of the list of songs and return None
    if i == len(list):
        return None    
    elif list[i].eliminated == False:
        return list[i]
    #if the song has been eliminated check the next one in the list
    else:
        return choicepicker(list,i+1)
    
   
#add the new favorite song to the list and remove it from the original
def newFave():
    for item in st.session_state.list:
        if item.eliminated == False:
            st.session_state.favs.append(item)
            st.session_state.list.remove(item)
            st.session_state.currentfav = item

    
#check if only one song is remaining
def isFinished():
    count = 0
    for item in st.session_state.list:
        if item.eliminated == False:
            count += 1
    if count > 1:
        return False
    else: 
        return True
    
def handle_choice(winner, loser):
    loser.elim(winner)
    st.session_state.elim_countdown += -1
    st.session_state.prev_choices.append(winner)
    st.session_state.prev_choices.append(loser)
     

def skip_choice():
    # random.shuffle(st.session_state.list)
    pass

def go_back():
    last_loser = st.session_state.prev_choices.pop(-1)
    print (last_loser.name)
    last_winner = st.session_state.prev_choices.pop(-1)
    last_loser.eliminated = False
    del last_loser.eliminators[-1]
    if st.session_state.list.index(last_loser) < st.session_state.list.index(last_winner):
        st.session_state.i = st.session_state.list.index(last_loser)
    else: 
        st.session_state.i = st.session_state.list.index(last_winner)
    st.session_state.elim_countdown += 1


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
        for item in st.session_state.list: st.session_state.favs.append(item)
    show_favs()

def stop_picking():
    st.session_state.list = []

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
    for item in st.session_state.favs:
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
        
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].subheader(f"**{item.name}**")
        count += 1    

def show_list():
    count = 1
    midcol = st.columns(3)
    midcol2 = st.columns([0.25,0.75,0.25])
    midcol[1].markdown(
    f"""
    <div style="text-align: center; font-size: 18px;">
        You chose these things:
    </div>
    """,
    unsafe_allow_html=True
    )    
    for item in st.session_state.list:
        listcont = midcol2[1].container(border=True,height=250)
        listcol = listcont.columns([0.1,0.6,0.3])

        listcol[0].write("")
        listcol[0].write("")
        listcol[0].write("")
        listcol[0].header(count)

        # listcol[2].image(image=song.cover,width=215)
        
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].write("")
        listcol[1].subheader(f"**{item.name}**")
        count += 1    
        
  

def link_entered(link):
    #split the link into its url fields and check the 4th element to see if user entered a playlist, album, or artist link
    link_split = link.split(", ")
    for item in link_split:
        new_item = items.item(item)
        st.session_state.list.append(new_item)
    st.session_state.state = 1
    st.rerun()
    # else:
    #     linkcol[1].write("Invalid Link. Please make sure the playlist is public and not empty.")

def change_playlist():
    st.session_state.list = []
    st.session_state.Link = ""
    st.session_state.state = 0
    # st.session_state.change = False

def start_picking():
    st.session_state.state = 2
    random.shuffle(st.session_state.list)

pagecol = st.columns([0.25,0.75,0.25])
pagecol[1].markdown(
    """
    <h1 style="text-align: center;">🎵 Pick Your Favorite! 🎵</h1>
    """,
    unsafe_allow_html=True
)

listcol = st.columns([0.40,0.5,0.40])

if st.session_state.state == 0:
    link = listcol[1].text_input("Please enter in a comma separated list of things you want to pick from.",
                     key = "List",
                    #  on_change =lambda: link_entered(link)
                     )
    if link != "":
        link_entered(link)

elif st.session_state.state == 1:
    st.session_state.elim_countdown = len(st.session_state.list) - 1
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
    change = start[2].button(
        label = "Change List",
        key="change",
        on_click=lambda:change_playlist()
    )    
    show_list()

else:
    favcount = len(st.session_state.favs)
    currenttotal = len(st.session_state.list)

    s = ""
    i = st.session_state.i

    #check if there is only one song remaining and skip the choosing 
    if len(st.session_state.list) > 1:

        if isFinished() == False:

            #pick the two choices that the user will choose from by iterating through the list
            choice1 = choicepicker(st.session_state.list,st.session_state.i)
            #if rest of the songs have been eliminated go through list from the beginning
            if choice1 == None: 
                st.session_state.i = 0
                choice1 = choicepicker(st.session_state.list,st.session_state.i)
            st.session_state.i = st.session_state.list.index(choice1) + 1
            choice2 = choicepicker(st.session_state.list,st.session_state.i)
            if choice2 == None:
                st.session_state.i = 0
                choice2 = choicepicker(st.session_state.list,st.session_state.i)
            st.session_state.i = st.session_state.list.index(choice2) + 1



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
            cont1.markdown(f"**{choice1.name}**")
            cont1col = cont1.columns([0.75,0.25])
            cont1col[0].button(
                label = "Select",
                key=f"choice1_{st.session_state.l}",
                on_click=lambda: handle_choice(choice1, choice2)
            )


            cont2 = col[2].container(
                border=True,
                height=580
            )
            cont2.markdown(f"**{choice2.name}**")
            cont2col = cont2.columns([0.75,0.25])
            cont2col[0].button(
                label = "Select",
                key=f"choice2_{st.session_state.l+1}",
                on_click=lambda: handle_choice(choice2, choice1)
            )          
            st.session_state.l += 1


            skipbackcol = st.columns([0.3,0.6,0.25])
            skipback = skipbackcol[1].columns([0.2,0.1,0.1,0.2])

            # skipcol = st.columns([1.24,0.1,1.24])
            skipback[1].button(
                    label="Skip",
                    key=f"skip_{st.session_state.get('l', 0)}",
                    on_click=lambda:skip_choice()
                )
            if st.session_state.elim_countdown != len(st.session_state.list) -1:
                skipback[2].button(
                        label="Back",
                        key=f"Back{st.session_state.get('l', 0)}",
                        on_click=lambda:go_back()
                    )            



        else:
            newFave()

            #check if there is only one song left and rerun if there is
            if len(st.session_state.list) == 1:
                st.rerun()

            #make it so songs that were eliminated by last favorite are now marked as not eliminated
            itemcount = 0
            thissong = "" #placeholder for current song when iterating
            for item in st.session_state.list:
                if item.eliminators[-1] == st.session_state.currentfav:
                    item.eliminated = False
                    thisitem0 = item
                    itemcount += 1
            #checks if there is only one song that was eliminated by the current fav            
            if itemcount < 2:
                st.rerun()
            st.session_state.elim_countdown = itemcount - 1 #set countdown to how many songs are to be shown next 


            # # ensure that even if last 2 choices are properly asked even if they haven't been eliminated by the same song
            # if len(st.session_state.list) < 3:
            #     if st.session_state.list[0].eliminator == st.session_state.list[1]:
            #     for song in st.session_state.list:
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
            #plan to add back button even on fav showing screen
            # backcol = st.columns([1.24,0.1,1.24])
            # backcol[1].button(
            #             label="Back",
            #             key=f"Back2{st.session_state.get('l', 0)}",
            #             on_click=lambda:go_back()
            #         )

    elif len(st.session_state.list) == 1: end_of_game(True)
    else: end_of_game(False)