from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.button import Button
from kivy.metrics import dp
import webbrowser

class AnimeDetailsScreen(Screen):
    title = StringProperty('')
    description = StringProperty('')
    banner_url = StringProperty('')
    trailer_url = StringProperty('')
    watch_url = StringProperty('')
    status = StringProperty('planned')
    status_text = StringProperty('Запланировано')
    status_color = ListProperty([0.3, 0.3, 1, 1])
    rating = NumericProperty(0)
    rating_text = StringProperty('Нет оценки')
    rating_color = ListProperty([0.7, 0.7, 0.7, 1])
    tags = StringProperty('')
    anime_id = NumericProperty(0)
    db = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AnimeDetailsScreen, self).__init__(**kwargs)
        self.name = 'anime_details'
        
    def load_anime(self, anime_data):
        """Загружает данные аниме на страницу"""
        self.title = anime_data.get('title', '')
        self.description = anime_data.get('description', '')
        self.banner_url = anime_data.get('banner_url', '')
        self.trailer_url = anime_data.get('trailer_url', '')
        self.watch_url = anime_data.get('watch_url', '')
        self.status = anime_data.get('status', 'planned')
        self.rating = anime_data.get('rating', 0)
        self.tags = anime_data.get('tags', '')
        self.anime_id = anime_data.get('anime_id', 0)
        self.db = anime_data.get('db', None)
        self.update_status_text()
        self.update_rating_text()

    def open_trailer(self):
        """Открывает ссылку на трейлер в браузере"""
        if self.trailer_url:
            webbrowser.open(self.trailer_url)

    def open_watch_link(self):
        """Открывает ссылку для просмотра в браузере"""
        if self.watch_url:
            webbrowser.open(self.watch_url)

    def update_status(self, new_status):
        """Обновляет статус просмотра"""
        if self.db:
            self.db.update_anime_status(self.anime_id, new_status)
            self.status = new_status
            self.update_status_text()

    def update_rating(self, new_rating):
        """Обновляет рейтинг"""
        if self.db:
            self.db.update_anime_rating(self.anime_id, new_rating)
            self.rating = new_rating
            self.update_rating_text()

    def go_back(self):
        """Возвращается на главный экран"""
        self.manager.current = 'main'

    def update_status_text(self):
        """Обновляет текстовое представление статуса"""
        status_map = {
            'planned': ('Запланировано', [0.3, 0.3, 1, 1]),
            'watching': ('Смотрю', [1, 0.6, 0.2, 1]),
            'completed': ('Просмотрено', [0.2, 0.8, 0.2, 1])
        }
        self.status_text, self.status_color = status_map.get(self.status, ('', [0.7, 0.7, 0.7, 1]))

    def update_rating_text(self):
        """Обновляет текстовое представление рейтинга"""
        if self.rating > 0:
            self.rating_text = f'{self.rating} ★'
            self.rating_color = [1, 0.8, 0.2, 1]
        else:
            self.rating_text = 'Нет оценки'
            self.rating_color = [0.7, 0.7, 0.7, 1] 