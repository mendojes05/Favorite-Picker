import streamlit as st

home_page = st.Page("home_page.py", title = "Home")
spotify_page = st.Page("spotify_picker.py", title = "Spotify Picker")
custom_list_page = st.Page("custom_list.py", title = "Custom List Picker")

# Set up navigation
pg = st.navigation([home_page, spotify_page, custom_list_page])

# Run the selected page
pg.run()
