from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.98, 0.98, 0.98, 1)
        self.cursor_color = (0.2, 0.2, 0.3, 1)
        self.foreground_color = (0.2, 0.2, 0.3, 1)
        self.padding = [dp(10), dp(10)]
        self.font_size = dp(16)

class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.font_size = dp(16)
        self.bold = True

class AddAnimeForm(BoxLayout):
    def __init__(self, add_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        self.add_callback = add_callback

        # Заголовок
        self.add_widget(Label(
            text='Добавить аниме',
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.2, 0.3, 1)
        ))

        # Создаем поля ввода
        self.title_input = CustomTextInput(
            hint_text='Название аниме',
            multiline=False,
            size_hint_y=None,
            height=dp(45)
        )

        self.description_input = CustomTextInput(
            hint_text='Описание',
            multiline=True,
            size_hint_y=None,
            height=dp(90)
        )

        self.banner_input = CustomTextInput(
            hint_text='Ссылка на баннер',
            multiline=False,
            size_hint_y=None,
            height=dp(45)
        )

        self.trailer_input = CustomTextInput(
            hint_text='Ссылка на трейлер',
            multiline=False,
            size_hint_y=None,
            height=dp(45)
        )

        self.watch_link_input = CustomTextInput(
            hint_text='Ссылка на просмотр',
            multiline=False,
            size_hint_y=None,
            height=dp(45)
        )

        self.tags_input = CustomTextInput(
            hint_text='Теги (через запятую)',
            multiline=False,
            size_hint_y=None,
            height=dp(45)
        )

        # Добавляем все элементы в форму
        self.add_widget(self.title_input)
        self.add_widget(self.description_input)
        self.add_widget(self.banner_input)
        self.add_widget(self.trailer_input)
        self.add_widget(self.watch_link_input)
        self.add_widget(self.tags_input)

        # Кнопки
        button_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        add_button = CustomButton(
            text='Добавить',
            background_color=(0.2, 0.6, 1, 1)
        )
        add_button.bind(on_press=self.on_add)
        
        cancel_button = CustomButton(
            text='Отмена',
            background_color=(0.9, 0.9, 0.93, 1),
            color=(0.3, 0.3, 0.4, 1)
        )
        cancel_button.bind(on_press=self.on_cancel)

        button_layout.add_widget(add_button)
        button_layout.add_widget(cancel_button)
        self.add_widget(button_layout)

    def on_add(self, instance):
        """Собирает данные из формы и передает их в callback"""
        anime_data = {
            "title": self.title_input.text,
            "description": self.description_input.text,
            "banner": self.banner_input.text,
            "trailer": self.trailer_input.text,
            "watch_link": self.watch_link_input.text,
            "tags": self.tags_input.text
        }
        self.add_callback(anime_data)

    def on_cancel(self, instance):
        """Закрывает форму без сохранения"""
        # Ищем родительский Popup и закрываем его
        parent = self.parent
        while parent and not hasattr(parent, 'dismiss'):
            parent = parent.parent
        if parent:
            parent.dismiss()
