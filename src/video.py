import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('MY_YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

    def __init__(self, video_id):
        self.video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=video_id
                                                ).execute()
        self.video_id = video_id
        self.title: str = self.video['items'][0]['snippet']['title']
        self.url: str = self.video['items'][0]['snippet']['thumbnails']['default']['url']
        self.view_count: int = int(self.video['items'][0]['statistics']['viewCount'])
        self.like_count: int = self.video['items'][0]['statistics']['likeCount']

    def __repr__(self):
        return f'{self.video}\n{self.title}\n{self.url}\n{self.view_count}\n{self.like_count}'

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.playlist_id = playlist_id


video1 = Video('AWX4JnAnjBE')
print(video1)
video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
print(video2)
