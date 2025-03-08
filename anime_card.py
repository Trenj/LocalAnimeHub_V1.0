from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
import webbrowser

class AnimeCard(BoxLayout):
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
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AnimeCard, self).__init__(**kwargs)
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.banner_url = kwargs.get('banner_url', '')
        self.trailer_url = kwargs.get('trailer_url', '')
        self.watch_url = kwargs.get('watch_url', '')
        self.status = kwargs.get('status', 'planned')
        self.rating = kwargs.get('rating', 0)
        self.tags = kwargs.get('tags', '')
        self.anime_id = kwargs.get('anime_id', 0)
        self.db = kwargs.get('db', None)
        self.app = kwargs.get('app', None)
        self.update_status_text()
        self.update_rating_text()

    def show_details(self):
        """Переходит на детальную страницу аниме"""
        if self.app:
            anime_data = {
                'title': self.title,
                'description': self.description,
                'banner_url': self.banner_url,
                'trailer_url': self.trailer_url,
                'watch_url': self.watch_url,
                'status': self.status,
                'rating': self.rating,
                'tags': self.tags,
                'anime_id': self.anime_id,
                'db': self.db
            }
            self.app.show_anime_details(anime_data)

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

    def update_tags(self, new_tags):
        """Обновляет теги"""
        if self.db:
            self.db.update_anime_tags(self.anime_id, new_tags)
            self.tags = new_tags

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