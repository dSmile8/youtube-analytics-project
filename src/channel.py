import os
import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('MY_YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.__channel_id = channel_id
        self.title: str = self.channel['items'][0]['snippet']['title']
        self.channel_info: str = self.channel['items'][0]['snippet']['description']
        self.url: str = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscribers_count: int = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count: int = self.channel['items'][0]['statistics']['videoCount']
        self.view_count: int = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other):
        return int(self.subscribers_count) - int(other.subscribers_count)

    def __gt__(self, other):
        return self.subscribers_count > other.subscribers_count

    def __ge__(self, other):
        return self.subscribers_count >= other.subscribers_count

    def __lt__(self, other):
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other):
        return self.subscribers_count <= other.subscribers_count

    def __eq__(self, other):
        return self.subscribers_count == other.subscribers_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(self.channel)

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, file_name):
        """Метод, сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        info_dict = {
            'chanel_id': self.__channel_id,
            'title': self.title,
            'channel_info': self.channel_info,
            'url': self.url,
            'subscribers_count': self.subscribers_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(file_name, "w") as f:
            json.dump(info_dict, f)
