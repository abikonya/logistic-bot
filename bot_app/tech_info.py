'''
Файл хранения технической информации (выбранный язык, позиция, оффсет и кол-во страниц ответа).

Technical information file (language, position, offset and pages of answer).
'''


from vedis import Vedis
import os


base_dir = os.path.dirname(os.path.abspath(__file__))


def set_language(telegram_id, language):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            user['language'] = language
        except Exception as err:
            print(err)


def return_language(telegram_id):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            return user['language'].decode('UTF-8')
        except Exception as err:
            print(err)


def set_position(telegram_id, position):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            user['position'] = position
        except Exception as err:
            print(err)


def return_position(telegram_id):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            return user['position'].decode('UTF-8')
        except Exception as err:
            print(err)


def set_offset(telegram_id, offset):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            user['offset'] = offset
        except Exception as err:
            print(err)


def return_offset(telegram_id):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            return user['offset'].decode('UTF-8')
        except Exception as err:
            print(err)


def set_pages(telegram_id, pages):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            user['pages'] = pages
        except Exception as err:
            print(err)


def return_pages(telegram_id):
    with Vedis(os.path.join(base_dir, 'tech_info.vdb')) as db:
        try:
            user = db.Hash(telegram_id)
            return user['pages'].decode('UTF-8')
        except Exception as err:
            print(err)
