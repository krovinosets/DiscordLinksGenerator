
class DataBase:

    def create_connection(self):
        print("Подключение создано")

    def insert(self, link: str) -> bool:
        print(f'Ссылка {link} добавлена в базу данных')
        return True