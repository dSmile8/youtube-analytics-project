import os
import isodate
import datetime
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('MY_YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                          part='snippet, contentDetails',
                                                          maxResults=50,
                                                          ).execute()
        self.channel_id = self.playlist['items'][0]['snippet']['channelId']
        self.playlists_info = self.youtube.playlists().list(channelId=self.channel_id,
                                                            part='contentDetails,snippet',
                                                            maxResults=50,
                                                            ).execute()
        for k in self.playlists_info['items']:
            if k['id'] == playlist_id:
                self.title = k['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={playlist_id}'

    def make_list_video_id(self):
        '''Делаем список id всех видео из плэйлиста'''
        video_ids = []
        for playlist in self.playlist['items']:
            video_ids.append(playlist['contentDetails']['videoId'])
        return video_ids

    @property
    def total_duration(self):
        """Получаем общую продолжительность видео плэйлиста"""
        video_ids = self.make_list_video_id()
        video_response = self.youtube.videos().list(part='contentDetails,statistics, snippet',
                                                    id=','.join(video_ids)
                                                    ).execute()

        total = datetime.timedelta(0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return (total)

    def show_best_video(self):
        '''Получаем самое популярное видео из плэйлиста'''
        view_dict = {}
        video_ids = self.make_list_video_id()  # Получаем список с id всех видео плэйлиста
        video_response = self.youtube.videos().list(part='contentDetails,statistics, snippet',
                                                    id=','.join(video_ids)
                                                    ).execute()
        for video in video_response['items']:
            view_dict[video['id']] = int(video['statistics']['viewCount'])  # Добавляем ключ: значение в словарь
            maximum = max(view_dict, key=view_dict.get)  # Ищем ключ с max значением value
        return f'https://youtu.be/{maximum}'
