from pytube import YouTube # Импортирование модуля YouTube.

youtube_video_url = 'https://www.youtube.com/watch?v=Gwvv7Z6kzRA' # Ссылка на видео.
yt_obj = YouTube(youtube_video_url) # Создание объекта с помощью модуля и ссылки на видео.   

# Метод для скачивания АУДИО с переданнм форматом:
def get_audio_from_youTube_video(extansion: str):
    try:
        yt_obj.streams.get_audio_only().download(filename=f'audio.{extansion}') # Формат можно заменить.
        print('YouTube audio downloaded successfully')
    except Exception as ex:
        print(ex)
    
# Метод для скачивания ВИДЕО с переданнм форматом:    
def get_video_from_youTube_video(extansion: str): 
    try: 
        yt_obj.streams.get_highest_resolution().download(filename=f"video.{extansion}") # Формат можно заменить.
        print('YouTube video downloaded successfully')
    except Exception as ex:
        print(ex)

get_video_from_youTube_video("mp4") # Получение видео-файла.
get_audio_from_youTube_video("wav") # Получение аудио-файла.



