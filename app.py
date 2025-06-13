import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the songs CSV
df = pd.read_csv("songs.csv")

# Streamlit UI
st.set_page_config(page_title="Mood-Based Music Recommender 🎧", layout="centered")
st.title("🎵 Mood-Based Music Recommender")
st.markdown("Tell us how you're feeling, and we'll match songs from **English**, **Hindi**, and **Punjabi** 🎶")

# Input mood
user_input = st.text_input("How are you feeling today?", placeholder="e.g., happy, sad, energetic...")

if user_input:
    # Combine moods for similarity check
    moods = df['mood'].tolist()
    combined = moods + [user_input]

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(combined)

    # Cosine similarity
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_index = similarity.argmax()
    matched_mood = moods[best_match_index]

    st.success(f"🎧 Detected Mood: **{matched_mood.capitalize()}**")
    st.markdown("Here are some songs for you:")

    # Filter top 6 songs (2 per language)
    filtered_songs = df[df['mood'] == matched_mood]

    for lang in ['English', 'Hindi', 'Punjabi']:
        lang_songs = filtered_songs[filtered_songs['language'] == lang].head(2)
        if not lang_songs.empty:
            st.subheader(f"🎼 {lang} Songs")
            for _, row in lang_songs.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(row['image_url'], width=100)
                with col2:
                    st.markdown(f"**{row['song']}**")
                    st.markdown(f"[▶️ Watch on YouTube]({row['youtube_link']})")

else:
    st.info("Please enter your current mood to get music suggestions 🎧")
