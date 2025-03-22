import streamlit as st
import pandas as pd
import pickle
import requests
import time
from io import BytesIO


# Apply custom CSS for button styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #28a745; /* Green background */
        color: white;  /* White text */
        border-radius: 5px;  /* Rounded corners */
        padding: 10px 20px; /* Padding */
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #218838; /* Darker green on hover */
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
# -------------------------------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------------------------------------

# Streamlit App UI
st.title("Movie Exploration")

st.write('''Welcome to the **movie exploration**website. Here, I have **4808** movies collection from **Hollywood**.
         Use this website to explore movie details, it helps you to **Get Details** of Movies, so olease enter or select a movie
         name & Other details''')

st.write('''My Other Projects :
            Retail Techstore Sales Analysis (Please Go through the link) : https://salesanalytics-somnath-techstore.streamlit.app/''')

st.write('''My other project link  (Bengali Audio Story Dictionary) :  https://bengaliaudiostorysomnathbanerjee.streamlit.app/''')

st.write('''My other project link  (Lok Sava) : https://loksavasomnath.streamlit.app/''')

st.image('cinemaimage08.jpg', caption='Welcome to Movie Exploration', use_container_width=True)

# -------------------------------------------------------------------------------------------------------------------

# Movie exploration section
st.title("Movie Exploration")

selected_movie_name_input = st.selectbox(
    '**Please** **Select** a **movie** **name** & **wait** for a **sec** :', 
    movies_oth['title'].values,
    key="movie_selectbox_1"
)

# When the user clicks on "Fetch Movie Details"
if st.button('Get Movie Details'):
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
            st.image(movie_details['poster'], caption=f"Poster of {movie_details['title']}", use_container_width=True)
            st.write("**Movie** **Details** **given** **Successfully!**")
        else:
            st.write('Sorry, no details found for this movie.')
    else:
        st.write("Please select a movie to get details.")

# -------------------------------------------------------------------------------------------------------------------
# GitHub raw URL for the Excel file
movie_data_url = "https://raw.githubusercontent.com/Somnath342000/Movie_Exploration_Suggestion/main/hollywoodmoviesdata.xlsx"

# Try fetching the data
try:
    # Make the request to get the file content
    response = requests.get(movie_data_url)
    
    if response.status_code == 200:
        st.success("Movie data loaded successfully from GitHub")
        
        # Load the Excel file into a pandas DataFrame
        df_movies = pd.read_excel(BytesIO(response.content), engine="openpyxl")

        # Filtering options for the movie data (same as before)
        selected_RANK = st.selectbox("Select RANK", ["All"] + df_movies["RANK"].unique().tolist())
        selected_genre1 = st.selectbox("Select Genre1", ["All"] + df_movies["genres1"].unique().tolist())
        selected_genre2 = st.selectbox("Select Genre2", ["All"] + df_movies["Generes2"].unique().tolist())
        selected_cast1 = st.selectbox("Select Cast", ["All"] + df_movies["cast1"].unique().tolist())
        selected_cast2 = st.selectbox("Select Cast", ["All"] + df_movies["cast2"].unique().tolist())
        selected_crew = st.selectbox("Select Director", ["All"] + df_movies["crew"].unique().tolist())

        # Apply filters based on user selections
        filtered_df = df_movies.copy()

        if selected_RANK != "All":
            filtered_df = filtered_df[filtered_df["RANK"] == selected_RANK]
        if selected_genre1 != "All":
            filtered_df = filtered_df[filtered_df["genres1"] == selected_genre1]
        if selected_genre2 != "All":
            filtered_df = filtered_df[filtered_df["Generes2"] == selected_genre2]
        if selected_cast1 != "All":
            filtered_df = filtered_df[filtered_df["cast1"] == selected_cast1]
        if selected_cast2 != "All":
            filtered_df = filtered_df[filtered_df["cast2"] == selected_cast2]
        if selected_crew != "All":
            filtered_df = filtered_df[filtered_df["crew"] == selected_crew]

        # Show filtered results in a table
        st.subheader("📌 Filtered Movie List")
        st.markdown(filtered_df[['title', 'crew', 'genres1', 'cast1', 'cast2', 'tagline', 'homepage']].to_html(escape=False), unsafe_allow_html=True)

    else:
        st.error(f"Failed to retrieve the file. HTTP Status code: {response.status_code}")

except Exception as e:
    st.error(f"An error occurred while processing the file: {e}")
# -----------------------------------------------------------------------------------------------------------------

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

# List of the first 6 images for the slideshow
image_paths_first_6 = [
    "cinemaimage04.jpg",
    "cinemaimage06.jpg",
    "cinemaimage07.jpg",
    "cinemaimage02.jpg",
    "cinemaimage05.jpg"
]

# Create a slideshow for the first 6 images with a 2-second interval
placeholder_1 = st.empty()  # Empty placeholder to refresh the image
for i in range(len(image_paths_first_6)):
    placeholder_1.image(image_paths_first_6[i], caption="Explore the Magic of Cinema", use_container_width=True)
    time.sleep(7)  # Wait for 7 seconds before displaying the next image

