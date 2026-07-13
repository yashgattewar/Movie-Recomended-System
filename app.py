import streamlit as st
import pickle
import requests

# =========================
# TMDB API KEY
# =========================
API_KEY = "488c485e48dc08040579359b57e40957"

# =========================
# LOAD DATA
# =========================
final = pickle.load(open('final.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# =========================
# FETCH MOVIE POSTER
# =========================
@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

        response = requests.get(url, timeout=20)

        if response.status_code == 200:
            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except Exception as e:
        print("Error:", e)
        return None
# =========================
# RECOMMENDATION FUNCTION
# =========================
def recomended(movie):
    movie_index = final[final['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = final.iloc[i[0]].movie_id

        recommended_movies.append(final.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a Movie",
    final['title'].values
)

if st.button("Recommend"):

    movie_names, movie_posters = recomended(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:

            if movie_posters[i]:
                st.image(movie_posters[i], width=220)
            else:
                # Empty space equal to poster height
                st.markdown(
                    """
                    <div style="
                        height:260px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        border:1px solid gray;
                        border-radius:10px;
                    ">
                        Poster Not Available
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-weight:bold;
                    min-height:60px;
                    margin-top:10px;
                ">
                    {movie_names[i]}
                </div>
                """,
                unsafe_allow_html=True
            )