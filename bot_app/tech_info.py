'''
Файл хранения технической информации (выбранный язык, позиция, оффсет и кол-во страниц ответа).

Technical information file (language, position, offset and pages of answer).
'''


from vedis import Vedis


class TechInfo:
    def __init__(self):
        self.db = Vedis(filename='tech_info.vdb', open_database=True)

    def set_language(self, telegram_id, language):
        user = self.db.Hash(telegram_id)
        user['language'] = language

    def return_language(self, telegram_id):
        user = self.db.Hash(telegram_id)
        return user['language'].decode('UTF-8')

    def set_position(self, telegram_id, position):
        user = self.db.Hash(telegram_id)
        user['position'] = position

    def return_position(self,telegram_id):
        user = self.db.Hash(telegram_id)
        return user['position'].decode('UTF-8')

    def set_offset(self, telegram_id, offset):
        user = self.db.Hash(telegram_id)
        user['offset'] = offset

    def return_offset(self, telegram_id):
        user = self.db.Hash(telegram_id)
        return user['offset'].decode('UTF-8')

    def set_pages(self, telegram_id, pages):
        user = self.db.Hash(telegram_id)
        user['pages'] = pages

    def return_pages(self, telegram_id):
        user = self.db.Hash(telegram_id)
        return user['pages'].decode('UTF-8')
