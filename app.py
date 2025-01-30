import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import time
import sqlite3

#-------------------------------------------------------------------------------------------------------------------

movie_dict_oth = pickle.load(open('movie_dict.pkl', 'rb'))  # Loading movie dictionary
# Convert the movie dictionary into a DataFrame
movies_oth = pd.DataFrame(movie_dict_oth)

# OMDb API key
OMDB_API_KEY = '2e632cd4'

# Function to fetch movie details and poster from OMDb API
def fetch_movie_details(movie_name):
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
#---------------------------------------------------------------------------------------------------------------------------------------------

# Streamlit App UI
st.title("Movie Exploration & Suggestion")

# Display Information 
st.write('''Hi friends! welcome to **movie** **exploration** & **suggestion** website Here, I have **4808** movies collection from **Hollywood**. 
         The movie information (titles, posters) used in this app is dragged from reliable sources such as **OMDb**Database. This site helps you to explore a movie details 
         in the initial section **Movie Exploration** by clicking the button **"Fetch Movie Details"** given bellow & aftter that
         you will be recommmend other movie based on your searching movie in the next section **Movie Suggestion** by clicking **"Recommend"** button''')

import streamlit as st
import time

# Define the list of image paths
image_list = [
    "cinemaimage04.jpg", 
    "cinemaimage06.jpg", 
    "cinemaimage01.jpg",
    "cinemaimage07.jpg",
    "cinemaimage03.jpg"
]

# Initialize session state for the image index (to keep track of the current image)
if 'image_index' not in st.session_state:
    st.session_state['image_index'] = 0

# Initialize session state for the last update time
if 'last_update_time' not in st.session_state:
    st.session_state['last_update_time'] = time.time()

# Create a placeholder for the image
image_placeholder = st.empty()

# Function to update the image
def update_image():
    current_index = st.session_state['image_index']
    image_placeholder.image(image_list[current_index], caption="Movie Exploration & Suggestion", use_container_width=True)

    # Increment the index for the next image
    next_index = (current_index + 1) % len(image_list)

    # Update the session state to the next image index
    st.session_state['image_index'] = next_index

# Timer to check the time difference (1 second delay)
if time.time() - st.session_state['last_update_time'] > 1:
    update_image()
    st.session_state['last_update_time'] = time.time()  # Update the last update time

# Run this to make sure the image changes when the page first loads
if 'image_index' in st.session_state:
    update_image()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

st.title("Movie Exploration")

# Display bold and larger text with Markdown
st.markdown(
    '''<span style="font-size: 18px; font-weight: bold;">Please Select a movie name & click on "Fetch Movie Details" button given bellow</span>''', 
    unsafe_allow_html=True
)

# Movie selection for fetching movie details using Streamlit's selectbox
selected_movie_name_input = st.selectbox(
    'Type a movie name here & wait for a few seconds:', 
    movies_oth['title'].values,
    key="movie_selectbox_1"  # Add a unique key for this selectbox
)

# When the user clicks on "Fetch Movie Details" button
if st.button('Fetch Movie Details'):
    if selected_movie_name_input:
        # Fetch the movie details and poster
        movie_details = fetch_movie_details(selected_movie_name_input)

        if movie_details:
            # Display movie details and poster
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
            st.image(movie_details['poster'], caption=f"Poster of {movie_details['title']}", use_container_width=True)
        else:
            st.write('''Sorry, no details found for this movie. 
                     Please check the movie name or try another one.''')
    else:
        st.write("Please enter a movie name to get details.")

#---------------------------------------------------------------------------------------------------------------------
# Function to fetch movie poster from OMDb API
def fetch_poster_omdb(movie_name):
    api_key = "2e632cd4"  # Your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_name.replace(' ', '+')}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['Response'] == 'True':
            return data['Poster']  # This will return the poster URL
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        return "https://via.placeholder.com/500x750?text=Request+Failed"

# Function to recommend similar movies
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []  # If the movie is not found, return empty lists for names and posters
    
    # Find the index of the movie in the DataFrame
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Get the similarity scores for that movie
    distances = similarity[movie_index]
    
    # Sort the movies based on the similarity scores, reverse=True to get highest first, and take top 5
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # Fetch the recommended movie titles and posters
    recommended_movies = []
    recommended_movie_posters = []  # List to hold poster URLs
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movie_posters.append(fetch_poster_omdb(movie_title))  # Fetch poster from OMDb API
    
    return recommended_movies, recommended_movie_posters

# Load the pickled data
try:
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))  # Loading movie dictionary
    similarity = pickle.load(open('similarity.pkl', 'rb'))  # Loading similarity matrix
except Exception as e:
    st.error(f"Error loading files: {e}")
    raise

# Convert the movie dictionary into a DataFrame
movies = pd.DataFrame(movie_dict)


# Display Information 
st.write('''Hollywood movies are available across various platforms:

1. **Theaters (Offline)**: Traditional cinema halls like **INOX** and **PVR**, as well as special formats like **IMAX**, showcase Hollywood films.
  
2. **Streaming Services (Online)**: Platforms like **Netflix**, **Amazon Prime Video**, **Disney+**, **HBO Max**, and **Apple TV+** offer a vast library of Hollywood movies for streaming.

3. **On-demand Rentals**: Services like **YouTube Movies**, **Google Play**, and **iTunes** allow users to rent or buy films.

4. **Cable & Satellite TV**: Channels like **HBO**, **Starz**, and **Showtime** air Hollywood movies.

5. **Physical Media**: Blu-ray/DVD still offers Hollywood films for home viewing. 

Streaming is now the most popular way to watch, but theaters and TV still play an important role. ''')

# Add an image inside a box with custom styling
st.image("cinemaimage08.jpg", caption="World of Cinema", use_container_width=True)
# ----------------------------------------------------------------------------------------------------------
# Title of the app
st.title("Movie Suggestion")

# Display introductory information
st.write('''Welcome to the Cinema Recommendation System !!
            Here you will be recommended movie as per your choice of selection''')

# Display bold and larger text with Markdown
st.markdown(
    '''<span style="font-size: 18px; font-weight: bold;">Please Select a movie name & click on "Recommend" button given bellow</span>''', 
    unsafe_allow_html=True
)

# Movie selection for recommendations using Streamlit's selectbox
selected_movie_name = st.selectbox(
    'Type a movie name here & wait for a few seconds:', 
    movies['title'].values,
    key="movie_selectbox_2"  # Add a unique key for this selectbox
)

# Button to trigger recommendations
if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    
    if recommendations:
        st.write("Recommended Movies:")
        col1, col2, col3, col4, col5 = st.columns(5)  # Create 5 columns for display
        st.markdown(
    '''<span style="font-size: 18px; font-weight: bold;">The recommendation is shown successfully!!</span>''', 
    unsafe_allow_html=True
)
        for i, movie in enumerate(recommendations):
            with locals()[f'col{i+1}']:  # Dynamically accessing columns
                st.text(movie)
                st.image(posters[i])  # Display movie poster
                
    else:
        st.write("Sorry, no recommendations found. Please check the movie name or try another one.")

# Display Information 
st.write('''**Hollywood** is a district in Los Angeles, California, known as the heart of the American film industry. 
It's where many major movie studios are based, and it's famous worldwide as the center of entertainment production, 
from film to television. Hollywood is home to iconic landmarks such as the Hollywood Sign and the Walk of Fame, 
and it has played a pivotal role in shaping global pop culture. ''')

# Add an image inside a box with custom styling
st.image("cinemaimage02.jpg", caption="Origin of Cinema", use_container_width=True)

# Display information about the history of cinema
st.write('''History of Movie:- 
The origins of cinema can be traced back to the late 19th century, with key pioneers such as Thomas Edison, 
the Lumière brothers, and Georges Méliès. Edison's invention of the Kinetoscope and the Lumière brothers' 
creation of the Cinématographe helped lay the groundwork for what would become the motion picture industry.
The first public screening of films by the Lumière brothers in 1895 is often considered the birth of cinema as we know it. 
Early films were silent and black-and-white, lasting only a few minutes.''')

# Add another image
st.image("cinemaimage05.jpg", caption="Enjoy the World of Cinema", use_container_width=True)

# Display information about genres and styles in cinema
st.write('''Genres and Styles:  
Cinema encompasses a wide variety of genres, each with its own conventions and styles. Some of the most popular include:

1. **Drama**: Focuses on serious, often emotional storytelling. It explores human conflict, relationships, and personal struggles.  
2. **Comedy**: Designed to entertain and amuse through humor, often characterized by light-hearted plots, witty dialogue, and physical comedy.  
3. **Action**: Features fast-paced, high-energy sequences, often involving physical stunts, chase scenes, or battles.  
4. **Horror**: Aims to evoke fear and suspense in the audience, using elements like dark lighting, eerie soundtracks, and supernatural or psychological threats.  
5. **Science Fiction**: Explores speculative concepts, often involving futuristic technology, space travel, and alternate realities.  
6. **Documentary**: Non-fiction films that depict real-life events, people, and situations, often with a focus on education or social issues.
''')

# Display introductory information
st.write('''This site is Created by <span style="font-size:20px; font-weight: bold;">Somnath Banerjee</span> using **python**  
            **Phone** : **91+ 6290693785** | **Mail** : somnathbanerjee342000@gmail.com
            **Linked IN Account** : https://www.linkedin.com/in/somnath-banerjee-9a91391a4 ''', unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------------------------------------------

# Feedback Section - Save Feedback to SQLite
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('moviefeedback.db')
cursor = conn.cursor()

# Create the feedback table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        feedback TEXT NOT NULL
    )
''')
conn.commit()

# Add a feedback section
st.write("## **We value your feedback!**")
feedback = st.text_area("Please leave your feedback here:")

# Email input for contact
email = st.text_input("Enter your email address:")

# When the 'Submit Feedback' button is pressed
if st.button('Submit Feedback'):
    if feedback and email:
        # Save feedback to the SQLite database
        cursor.execute('''
            INSERT INTO feedbacks (email, feedback) VALUES (?, ?)
        ''', (email, feedback))
        conn.commit()

        st.write(f"Thank you for your feedback, {email}!")
        st.write("Your feedback has been submitted successfully.")

        # Optionally, display the saved feedback for confirmation
        st.write(f"Feedback saved: {feedback}")
    else:
        st.error("Please provide both your email and feedback.")

# Close the connection to the database
conn.close()
