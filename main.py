from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from add_anime_form import AddAnimeForm
from database import AnimeDatabase
from anime_card import AnimeCard
from anime_details import AnimeDetailsScreen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.metrics import dp

# Загружаем файл стилей
Builder.load_file('styles.kv')

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.name = 'main'

class SearchBar(BoxLayout):
    search_callback = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)
        self.ids.search_input.bind(text=self.on_search_change)
        self.ids.status_filter.bind(text=self.on_search_change)
        self.ids.sort_by.bind(text=self.on_search_change)
    
    def on_search_change(self, instance, value):
        if self.search_callback:
            search_text = self.ids.search_input.text
            status = self.ids.status_filter.text
            sort_by = self.ids.sort_by.text
            self.search_callback(search_text, status, sort_by)

class AnimeHubApp(App):
    def build(self):
        # Устанавливаем цвет фона окна
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        
        self.db = AnimeDatabase()
        self.popup = None

        # Создаем менеджер экранов
        self.screen_manager = ScreenManager()

        # Создаем главный экран
        self.main_screen = MainScreen()
        self.root_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15))

        # Заголовок
        header = BoxLayout(size_hint_y=None, height=dp(70))
        header.add_widget(Label(
            text='Локальный Аниме Хаб',
            font_size=dp(28),
            bold=True,
            color=(1, 1, 1, 1)
        ))
        self.root_layout.add_widget(header)

        # Добавляем поисковую панель
        self.search_bar = SearchBar()
        self.search_bar.search_callback = self.on_search
        self.root_layout.add_widget(self.search_bar)

        # Область списка аниме
        self.scroll_view = ScrollView()
        self.anime_list = GridLayout(
            cols=3,
            spacing=dp(15),
            size_hint_y=None,
            padding=dp(15)
        )
        self.anime_list.bind(minimum_height=self.anime_list.setter('height'))
        self.scroll_view.add_widget(self.anime_list)
        self.root_layout.add_widget(self.scroll_view)

        # Загружаем сохранённые аниме
        self.load_anime()

        # Контейнер для кнопки добавления
        btn_layout = BoxLayout(
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            pos_hint={'right': 0.95, 'bottom': 0.05}
        )

        # Кнопка добавления аниме
        self.add_anime_btn = Button(
            text='+',
            font_size=dp(30),
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            background_color=(0.2, 0.6, 1, 1),
            background_normal=''
        )
        self.add_anime_btn.bind(on_press=self.open_add_anime_form)

        # Скругление углов кнопки
        with self.add_anime_btn.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.rounded_rect = RoundedRectangle(
                pos=self.add_anime_btn.pos,
                size=self.add_anime_btn.size,
                radius=[dp(30)]
            )

        self.add_anime_btn.bind(
            pos=self.update_rounded_rect,
            size=self.update_rounded_rect
        )

        btn_layout.add_widget(self.add_anime_btn)
        self.root_layout.add_widget(btn_layout)

        # Добавляем главный экран в менеджер
        self.main_screen.add_widget(self.root_layout)
        self.screen_manager.add_widget(self.main_screen)

        # Создаем экран деталей аниме
        self.details_screen = AnimeDetailsScreen()
        self.screen_manager.add_widget(self.details_screen)

        return self.screen_manager

    def on_search(self, search_text, status, sort_by):
        """Обработчик поиска и сортировки"""
        self.anime_list.clear_widgets()
        
        # Преобразуем значения фильтров
        status_map = {
            'Все': None,
            'Запланировано': 'planned',
            'Смотрю': 'watching',
            'Просмотрено': 'completed'
        }
        sort_map = {
            'По названию': 'title',
            'По рейтингу': 'rating',
            'По статусу': 'status'
        }
        
        status_filter = status_map.get(status)
        sort_field = sort_map.get(sort_by, 'title')
        
        # Получаем отфильтрованный список
        if search_text:
            anime_list = self.db.search_anime(search_text, status_filter)
        else:
            anime_list = self.db.get_all_anime(sort_by=sort_field)
        
        # Отображаем результаты
        for anime in anime_list:
            anime_id, title, description, banner, trailer, link, status, rating, tags = anime
            card = AnimeCard(
                anime_id=anime_id,
                title=title,
                description=description,
                banner_url=banner,
                trailer_url=trailer,
                watch_url=link,
                status=status,
                rating=rating,
                tags=tags,
                db=self.db,
                app=self
            )
            self.anime_list.add_widget(card)

    def load_anime(self):
        """Загружает сохранённые аниме в интерфейс"""
        self.anime_list.clear_widgets()
        for anime in self.db.get_all_anime():
            anime_id, title, description, banner, trailer, link, status, rating, tags = anime
            card = AnimeCard(
                anime_id=anime_id,
                title=title,
                description=description,
                banner_url=banner,
                trailer_url=trailer,
                watch_url=link,
                status=status,
                rating=rating,
                tags=tags,
                db=self.db,
                app=self
            )
            self.anime_list.add_widget(card)

    def add_anime(self, anime_data):
        """Добавляет аниме в базу и обновляет список"""
        try:
            self.db.add_anime(
                anime_data["title"],
                anime_data["description"],
                anime_data["banner"],
                anime_data["trailer"],
                anime_data["watch_link"],
                'planned',
                0,
                anime_data.get("tags", "")
            )
            self.load_anime()
        except Exception as e:
            print(f"Ошибка при добавлении в БД: {e}")
        finally:
            if self.popup:
                self.popup.dismiss()
                self.popup = None

    def update_rounded_rect(self, instance, value):
        """Обновляет положение и размер скругленного фона кнопки"""
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size

    def open_add_anime_form(self, instance):
        """Открывает форму добавления аниме"""
        content = AddAnimeForm(self.add_anime)
        self.popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.8),
            background='',
            background_color=(0.1, 0.1, 0.1, 1),
            separator_color=(0.2, 0.2, 0.2, 1)
        )
        self.popup.open()

    def show_anime_details(self, anime_data):
        """Показывает детальную страницу аниме"""
        self.details_screen.load_anime(anime_data)
        self.screen_manager.current = 'anime_details'

if __name__ == '__main__':
    AnimeHubApp().run()
