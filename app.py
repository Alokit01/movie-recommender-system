import pickle
import streamlit as st
import pandas as pd
import requests

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Recommender AI",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

session = requests.Session()

# ---------------- POSTER FUNCTION ---------------- #

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

        response = session.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None

    except:
        return None

# ---------------- RECOMMENDATION ---------------- #

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_names = []
    recommended_posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_names.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_names, recommended_posters

# ---------------- HEADER ---------------- #

st.markdown("""
<h1 style='text-align:center;'>
🎬 Movie Recommender AI
</h1>

<h4 style='text-align:center;color:gray;'>
Discover your next favorite movie in seconds
</h4>
""", unsafe_allow_html=True)

st.write("")

# ---------------- SEARCH ---------------- #

selected_movie = st.selectbox(
    "Search Movie",
    movies['title'].values,
    index=None,
    placeholder="🔍 Search movie here..."
)

st.write("")

# ---------------- BUTTON ---------------- #

if st.button("✨ Show Recommendations", use_container_width=True):

    if selected_movie:

        with st.spinner("🎥 Finding movies you'll love..."):

            names, posters = recommend(selected_movie)

        st.markdown("## 🍿 Recommended For You")

        cols = st.columns(5)

        for idx, col in enumerate(cols):

            with col:

                if posters[idx]:

                    st.image(
                        posters[idx],
                        use_container_width=True
                    )

                else:

                    st.info("Poster Not Available")

                st.markdown(
                    f"""
                    <div style="
                    text-align:center;
                    font-weight:600;
                    padding-top:10px;
                    ">
                    {names[idx]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ---------------- FOOTER ---------------- #

st.markdown("---")
