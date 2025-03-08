import sqlite3

class AnimeDatabase:
    def __init__(self, db_name="animehub.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Создаёт таблицу аниме, если её ещё нет"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                banner TEXT,
                trailer TEXT,
                link TEXT,
                status TEXT DEFAULT 'planned',
                rating INTEGER DEFAULT 0,
                tags TEXT
            )
        ''')
        self.connection.commit()

    def add_anime(self, title, description, banner, trailer, link, status='planned', rating=0, tags=''):
        """Добавляет аниме в базу"""
        self.cursor.execute('''
            INSERT INTO anime (title, description, banner, trailer, link, status, rating, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, banner, trailer, link, status, rating, tags))
        self.connection.commit()

    def get_all_anime(self, sort_by='title', sort_order='ASC'):
        """Получает список всех аниме с сортировкой"""
        valid_fields = ['title', 'rating', 'status']
        sort_field = sort_by if sort_by in valid_fields else 'title'
        order = 'DESC' if sort_order.upper() == 'DESC' else 'ASC'
        
        self.cursor.execute(f"SELECT * FROM anime ORDER BY {sort_field} {order}")
        return self.cursor.fetchall()

    def search_anime(self, query, status=None):
        """Поиск аниме по названию и описанию"""
        if status:
            self.cursor.execute("""
                SELECT * FROM anime 
                WHERE (title LIKE ? OR description LIKE ?) 
                AND status = ?
                ORDER BY title
            """, (f'%{query}%', f'%{query}%', status))
        else:
            self.cursor.execute("""
                SELECT * FROM anime 
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY title
            """, (f'%{query}%', f'%{query}%'))
        return self.cursor.fetchall()

    def update_anime_status(self, anime_id, status):
        """Обновляет статус просмотра аниме"""
        self.cursor.execute("""
            UPDATE anime SET status = ? WHERE id = ?
        """, (status, anime_id))
        self.connection.commit()

    def update_anime_rating(self, anime_id, rating):
        """Обновляет рейтинг аниме"""
        self.cursor.execute("""
            UPDATE anime SET rating = ? WHERE id = ?
        """, (rating, anime_id))
        self.connection.commit()

    def update_anime_tags(self, anime_id, tags):
        """Обновляет теги аниме"""
        self.cursor.execute("""
            UPDATE anime SET tags = ? WHERE id = ?
        """, (tags, anime_id))
        self.connection.commit()

    def close(self):
        """Закрывает соединение с базой данных"""
        self.connection.close()
