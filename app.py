import streamlit as st
import pandas as pd
import pickle
import requests
import sqlite3
from telegram import Bot
from PIL import Image
import os

# Telegram Bot Configuration (replace with your token)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"  # This can be your user ID or a group ID
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Inject custom CSS to hide Streamlit's header
st.markdown("""
    <style>
        .css-1y4j1cz {
            display: none;
        }
        .css-1g1jv04 {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

#-------------------------------------------------------------------------------------------------------------------
# Loading movie dictionary
movie_dict_oth = pickle.load(open('movie_dict.pkl', 'rb'))
movies_oth = pd.DataFrame(movie_dict_oth)

# OMDb API key
OMDB_API_KEY = '2e632cd4'

# Function to fetch movie details and poster from OMDb API
def fetch_movie_details(movie_name):
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data['Response'] == 'True':
            movie_details = {
                'title': data.get('Title'),
                'year': data.get('Year'),
                'genre': data.get('Genre'),
                'plot': data.get('Plot'),
                'poster': data.get('Poster'),
                'director': data.get('Director'),
                'actors': data.get('Actors'),
                'runtime': data.get('Runtime'),
                'rating': data.get('imdbRating'),
                'language': data.get('Language'),
                'country': data.get('Country'),
                'awards': data.get('Awards')
            }
            return movie_details
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching movie details: {e}")
        return None

# Function to fetch movie download link from Telegram (this should be adapted based on your Telegram bot setup)
def fetch_telegram_movie_download_link(movie_name):
    try:
        # Sample logic to fetch a download link (replace this with real logic)
        # Here we simulate the bot sending the movie download link via Telegram
        download_links = {
            "Movie1": "https://t.me/your_movie_bot/123",
            "Movie2": "https://t.me/your_movie_bot/124",
            "Movie3": "https://t.me/your_movie_bot/125"
        }

        link = download_links.get(movie_name, None)

        if link:
            bot.send_message(chat_id=CHAT_ID, text=f"Download Link for {movie_name}: {link}")
            return link
        else:
            return "No download link found for this movie."
    except Exception as e:
        st.error(f"Error sending message to Telegram: {e}")
        return "Error sending download link."

#-------------------------------------------------------------------------------------------------------------------
# Streamlit App UI
st.title("Movie Exploration & Suggestion")

# Display Information
st.write('''Welcome to the **movie exploration** & **suggestion** website. Here, I have **4808** movies collection from **Hollywood**.
         Use this website to explore movie details, get movie download links via Telegram, and get movie recommendations!''')

# Movie exploration section
st.title("Movie Exploration")

selected_movie_name_input = st.selectbox(
    'Select a movie name:', 
    movies_oth['title'].values,
    key="movie_selectbox_1"
)

# When the user clicks on "Fetch Movie Details"
if st.button('Fetch Movie Details'):
    if selected_movie_name_input:
        movie_details = fetch_movie_details(selected_movie_name_input)

        if movie_details:
            st.subheader(f"Movie: {movie_details['title']} ({movie_details['year']})")
            st.write(f"**Genre**: {movie_details['genre']}")
            st.write(f"**Plot**: {movie_details['plot']}")
            st.write(f"**Director**: {movie_details['director']}")
            st.write(f"**Actors**: {movie_details['actors']}")
            st.write(f"**Runtime**: {movie_details['runtime']}")
            st.write(f"**IMDb Rating**: {movie_details['rating']}")
            st.write(f"**Language**: {movie_details['language']}")
            st.write(f"**Country**: {movie_details['country']}")
            st.write(f"**Awards**: {movie_details['awards']}")
            
            poster_url = movie_details['poster'] if movie_details['poster'] != "N/A" else "https://via.placeholder.com/500x750?text=No+Poster+Available"
            st.image(poster_url, caption=f"Poster of {movie_details['title']}", use_container_width=True)
        else:
            st.write('Sorry, no details found for this movie.')
    else:
        st.write("Please select a movie to get details.")

# Movie suggestion section
st.title("Movie Suggestion")

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:', 
    movies_oth['title'].values,
    key="movie_selectbox_2"
)

if st.button('Recommend'):
    # Sample function to simulate recommendations (replace with actual recommendation logic).
    def recommend(movie):
        return ["Movie A", "Movie B", "Movie C"], ["poster_a.jpg", "poster_b.jpg", "poster_c.jpg"]
    
    recommendations, posters = recommend(selected_movie_name)
    
    if recommendations:
        st.write("Recommended Movies:")
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, movie in enumerate(recommendations):
            with locals()[f'col{i+1}']:
                st.text(movie)
                st.image(posters[i])
    else:
        st.write("Sorry, no recommendations found.")

# Telegram bot section - send movie download link to Telegram
st.title("Get Movie Download Link via Telegram")

movie_name_for_download = st.selectbox(
    'Select a movie to get download link from Telegram:', 
    movies_oth['title'].values,
    key="movie_selectbox_for_download"
)

if st.button('Get Download Link'):
    if movie_name_for_download:
        download_link = fetch_telegram_movie_download_link(movie_name_for_download)
        if download_link:
            st.write(f"Download link for {movie_name_for_download}: {download_link}")
        else:
            st.write("No download link found for this movie.")
    else:
        st.write("Please select a movie to get the download link.")

#-------------------------------------------------------------------------------------------------------------------
# Feedback Section - Save Feedback to SQLite
conn = sqlite3.connect('moviefeedback.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        feedback TEXT NOT NULL
    )
''')
conn.commit()

st.write("## **We value your feedback!**")
feedback = st.text_area("Please leave your feedback here:")
email = st.text_input("Enter your email address:")

if st.button('Submit Feedback'):
    if feedback and email:
        cursor.execute('''
            INSERT INTO feedbacks (email, feedback) VALUES (?, ?)
        ''', (email, feedback))
        conn.commit()

        st.write(f"Thank you for your feedback, {email}!")
        st.write("Your feedback has been submitted successfully.")
    else:
        st.error("Please provide both your email and feedback.")

conn.close()

# Display Information about Hollywood
st.write('''Hollywood is a district in Los Angeles, California, known as the heart of the American film industry. 
It's where many major movie studios are based, and it's famous worldwide as the center of entertainment production.''')
