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
        self.video_count: int = self.channel['items'][0]['statistics']['viewCount']
        self.view_count: int = self.channel['items'][0]['statistics']['videoCount']

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
        """Сохраняет данные в JSON-файл"""

        with open(file_name, "a") as f:
            # if os.stat(file_name).st_size == 0:
            json.dump(self.channel, f)
