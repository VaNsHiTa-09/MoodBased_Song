import pandas as pd

df = pd.read_csv("songs.csv")

# Auto-generate thumbnail from YouTube link
def extract_video_id(link):
    if 'youtu.be/' in link:
        return link.split('youtu.be/')[-1]
    elif 'watch?v=' in link:
        return link.split('watch?v=')[-1]
    else:
        return ''

df['image_url'] = df['youtube_link'].apply(lambda x: f"https://i.ytimg.com/vi/{extract_video_id(x)}/hqdefault.jpg")

df.to_csv("songs.csv", index=False)
print("✅ Thumbnails updated successfully.")
