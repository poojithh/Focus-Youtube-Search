from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

# create youtube API connection
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def search_youtube(query):

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=5
    )

    response = request.execute()

    videos = []

    for item in response["items"]:

        video = {
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }

        videos.append(video)

    return videos


# test block
if __name__ == "__main__":

    results = search_youtube("python tutorial")

    for video in results:
        print(video["title"], video["video_id"])