'''
Файл переводов.

Translations file.
'''


from vedis import Vedis
import os


base_dir = os.path.dirname(os.path.abspath(__file__))



def add_translation(name, language, translation):
    with Vedis(os.path.join(base_dir, 'localization.vdb')) as db:
        try:
            position = db.Hash(name)
            position[language] = translation
        except Exception as err:
            print(err)


def return_translation(name, language):
    with Vedis(os.path.join(base_dir, 'localization.vdb')) as db:
        try:
            position = db.Hash(name)
            return position[language].decode('UTF-8')
        except Exception as err:
            print(err)


def return_all_translations(name):
    with Vedis(os.path.join(base_dir, 'localization.vdb')) as db:
        try:
            answer = []
            position = db.Hash(name)
            for each in position.values():
                answer.append(each.decode('UTF-8'))
            return answer
        except Exception as err:
            print(err)


# Installed translations: 'en', 'ru'

translations = [
    ['rules', 'en', 'Read rules before using'],
    ['rules', 'ru', 'Прочтите правила использования бота - (ссылка на правила)'],
    ['rules_button', 'en', 'Agree'],
    ['rules_button', 'ru', 'С правилами ознакомлен'],
    ['zip_searching', 'en', 'Enter command /zip to search Zip-code'],
    ['zip_searching', 'ru', 'Введите команду /zip для поиска необходимого Zip-кода'],
    ['enter_zipcode', 'en', 'Enter zip'],
    ['enter_zipcode', 'ru', 'Введите цифровой номер (Zip-код)'],
    ['zip_not_found', 'en', 'Entered zip not found'],
    ['zip_not_found', 'ru', 'Введенный zip не найден'],
    ['server_error', 'en', 'Server error. Try later'],
    ['server_error', 'ru', 'Ошибка сервера. Попробуйте позже'],
    ['zip_list_choose', 'en', 'Make your choice please:'],
    ['zip_list_choose', 'ru', 'Выберите один из Zip-ов'],
    ['zip_list', 'en', 'You selected - {}'],
    ['zip_list', 'ru', 'Вы выбрали - {}'],
    ['zip_list_button', 'en', 'Show list of goods'],
    ['zip_list_button', 'ru', 'Посмотреть список товаров'],
    ['choose_category', 'en', 'Choose category of your product'],
    ['choose_category', 'ru', 'Выберите категорию Вашего товара'],
    ['choose_item', 'ru', 'Выберите Ваш товар'],
    ['choose_item', 'en', 'Choose your product'],
    ['chosen_zip_approve', 'en', 'Confirm'],
    ['chosen_zip_approve', 'ru', 'Принять'],
    ['chosen_zip_reset', 'en', 'Reset'],
    ['chosen_zip_reset', 'ru', 'Сбросить'],
    ['about_cargo', 'en', 'Enter product info'],
    ['about_cargo', 'ru', 'Введите информацию о товаре'],
    ['pickup_location', 'en', 'Pickup Location'],
    ['pickup_location', 'ru', 'Точка погрузки'],
    ['store_name', 'en', 'Store name'],
    ['store_name', 'ru', 'Название магазина'],
    ['store_phone', 'en', 'Store phone(optional)'],
    ['store_phone', 'ru', 'Телефонный номер магазина (если есть)'],
    ['order_number', 'en', 'Order number'],
    ['order_number', 'ru', 'Номер заказа'],
    ['pickup_person', 'en', 'Pickup person'],
    ['pickup_person', 'ru', 'Получатель'],
    ['additional_info', 'en', 'Any additional information required for pick up(optional)'],
    ['additional_info', 'ru', 'Дополнительная информация'],
    ['product_name', 'en', 'Product name'],
    ['product_name', 'ru', 'Название товара'],
    ['price', 'en', 'Price'],
    ['price', 'ru', 'Цена'],
    ['send_button', 'en', 'Send'],
    ['send_button', 'ru', 'Отправить'],
    ['all_is_done', 'en', 'The data entered is correct'],
    ['all_is_done', 'ru', 'Введенные данные верны'],
    ['success', 'en', 'Order created success! Your order-ID:'],
    ['success', 'ru', 'Заказ успешно создан! Ваш ID-заказа:'],
    ['success_button', 'en', 'Main menu'],
    ['success_button', 'ru', 'Главное меню'],
    ['status_checking', 'en', 'Enter command /status to check status of order'],
    ['status_checking', 'ru', 'Введите команду /status для просмотра статуса заказа'],
    ['enter_id', 'en', 'Enter order-ID:'],
    ['enter_id', 'ru', 'Введите ID-заказа'],
    ['status', 'en', "Your order's status"],
    ['status', 'ru', 'Статус Вашего заказа'],
    ['status_process', 'en', 'Process'],
    ['status_process', 'ru', 'В процессе'],
    ['status_confirm', 'en', 'Confirm'],
    ['status_confirm', 'ru', 'Исполнено'],
    ['status_cancel', 'en', 'Rejected'],
    ['status_cancel', 'ru', 'Отклонено'],
    ['enter_requisites', 'en', 'Enter your payment requisites'],
    ['enter_requisites', 'ru', 'Введите свои платежные реквизиты'],
    ['enter_requisites_button', 'en', 'Send'],
    ['enter_requisites_button', 'ru', 'Отправить'],
    ['payment_info', 'en', 'Information about payments'],
    ['payment_info', 'ru', 'Информация о расчетах'],
    ['paid_status', 'en', 'Paid'],
    ['paid_status', 'ru', 'Оплачено']
]


def update_translations(list_of_translations):
    count = 0
    for each in list_of_translations:
        add_translation(name=each[0], language=each[1], translation=each[2])
        count += 1

    print('Done. Added or update {} translations'.format(count))


if __name__ == '__main__':
    update_translations(translations)
