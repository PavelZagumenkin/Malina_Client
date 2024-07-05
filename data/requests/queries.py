class Queries:
    @staticmethod
    # Регистрация нового пользователя
    def register_user():
        return '''
        INSERT INTO users (username, password)
        VALUES (%s, %s);
        '''

    @staticmethod
    # Регистрация прав нового пользователя
    def register_role():
        return '''
        INSERT INTO users_role (username, role)
        VALUES (%s, %s);
        '''

    @staticmethod
    # Получить имя пользователя из БД
    def get_user_by_username():
        return '''
        SELECT * FROM users WHERE username = %s;
        '''

    @staticmethod
    # Получить права пользователя из БД
    def get_user_role_by_username():
        return '''
        SELECT role FROM users_role WHERE username = %s;
        '''

    @staticmethod
    # Получить количество строк в таблице user_role
    def get_rows_user_role():
        return '''
        SELECT COUNT(*) FROM users_role;
        '''

    @staticmethod
    # Получить роли всех пользователей с именами в таблице user_role
    def get_users_role():
        return '''
        SELECT * FROM users_role;
        '''

    @staticmethod
    # Установить новый пароль
    def new_password():
        return '''
        UPDATE users
        SET password = %s
        WHERE username = %s;
        '''

    @staticmethod
    # Установить новую роль
    def new_role():
        return '''
        UPDATE users_role
        SET role = %s
        WHERE username = %s;
        '''

    @staticmethod
    # Удалить пользователя из БД
    def delete_user():
        return '''
        DELETE FROM users_role
        WHERE username = %s;
        
        DELETE FROM users
        WHERE username = %s;
        '''

    @staticmethod
    # Запись лога
    def log_entry():
        return '''
        INSERT INTO logs (date, time, log)
        VALUES (%s, %s, %s);
        '''

    @staticmethod
    # Получить количество строк в таблице logs
    def get_rows_logs():
        return '''
        SELECT COUNT(*)
        FROM logs
        WHERE date >= %s AND date <= %s;
        '''

    @staticmethod
    # Получить все логи
    def get_logs():
        return '''
        SELECT * FROM logs
        WHERE date >= %s AND date <= %s;
        '''

    @staticmethod
    # Удалить логи из БД за период
    def delete_logs():
        return '''
        DELETE FROM logs
        WHERE date BETWEEN %s AND %s;
        '''

    @staticmethod
    # Получить имя пользователя из БД
    def get_version():
        return '''
         SELECT * FROM version;
         '''

    @staticmethod
    # Получить количество строк в таблице user_role
    def get_rows_konditerskie():
        return '''
        SELECT COUNT(*) FROM konditerskie;
        '''

    @staticmethod
    # Получить имя пользователя из БД
    def get_konditerskay_by_name():
        return '''
        SELECT * FROM konditerskie WHERE name = %s;
        '''

    @staticmethod
    # Регистрация новой кондитерской
    def register_konditerskay_in_DB():
        return '''
        INSERT INTO konditerskie (name, type, bakery, ice_sklad, vhod_group, tualet, stoliki, enable, bakery_store)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 1, %s);
        '''

    @staticmethod
    # Получить список кондитерских со всеми данными
    def get_konditerskie_in_DB():
        return '''
        SELECT * FROM konditerskie;
        '''

    @staticmethod
    # Установить новую роль
    def update_konditerskay_in_DB():
        return '''
        UPDATE konditerskie
        SET type = %s,
            bakery = %s,
            ice_sklad = %s,
            vhod_group = %s,
            tualet = %s,
            stoliki = %s,
            enable = %s,
            bakery_store = %s
        WHERE name = %s;
        '''

    @staticmethod
    # Получить количество строк из таблицы прогноз
    def get_count_row_prognoz_in_DB():
        return '''
        SELECT COUNT(*) FROM prognoz
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    # Получить количество строк из таблицы коэффицентов по дням недели
    def get_count_row_koeff_day_week_in_DB():
        return '''
        SELECT COUNT(*) FROM koeff_day_week
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    # Получить количество строк из таблицы нормативов
    def get_count_row_normativ_in_DB():
        return '''
        SELECT COUNT(*) FROM normativ_bakery
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    # Получить все блюда
    def get_data_tovar_in_DB():
        return '''
        SELECT * FROM dishes WHERE kod = %s;
        '''

    @staticmethod
    # Регистрация нового блюда в БД
    def insert_data_tovar_in_DB():
        return '''
        INSERT INTO dishes (kod, name, category, display, kvant, batch, koeff_ice_sklad)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''

    @staticmethod
    # Сохранение прогноза в БД
    def save_prognoz_in_DB():
        return '''
            INSERT INTO prognoz (period, name_point, kod_dishe, category, koeff_dishe,  display, kvant, batch, koeff_point, data_null, data_prognoz, author)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''

    @staticmethod
    # Удалить прогноз из БД
    def delete_prognoz_in_DB():
        return '''
        DELETE FROM prognoz
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    # Сохранение прогноза в БД
    def save_koeff_day_week_in_DB():
        return '''
            INSERT INTO koeff_day_week (period, name_point, category, day_week, koeff_day_week, koeff_point, data_null, data_koeff_day_week, author)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''

    @staticmethod
    # Получить список кондитерских в таблице прогноз за период
    def get_spisok_konditerskih_in_prognoz_in_DB():
        return '''
            SELECT DISTINCT name_point
            FROM prognoz
            WHERE period = %s AND category = %s;
            '''

    @staticmethod
    # Получить список кондитерских в таблице коэффицентов по дням недели за период
    def get_spisok_konditerskih_in_koeff_day_week_in_DB():
        return '''
            SELECT DISTINCT name_point
            FROM koeff_day_week
            WHERE period = %s AND category = %s;
            '''

    @staticmethod
    # Получить список категорий
    def get_spisok_category_in_DB():
        return '''
                SELECT DISTINCT category_dishes
                FROM category_dishes
                '''

    @staticmethod
    # Изменить наименование блюда
    def update_name_dishe_in_DB():
        return '''
        UPDATE dishes
        SET name = %s
        WHERE kod = %s;
        '''

    @staticmethod
    # Получить список всех блюд
    def spisok_kods_dishes_in_DB():
        return '''
        SELECT * FROM dishes;
        '''

    @staticmethod
    def spisok_name_dishes_in_DB(placeholders):
        return f'''
        SELECT name FROM dishes WHERE kod IN ({placeholders})
        '''

    @staticmethod
    # Получить все блюда
    def get_kod_dishe_in_DB():
        return '''
        SELECT * FROM dishes WHERE name = %s;
        '''

    @staticmethod
    # Получить прогноз продаж за период, выбранной категории
    def get_prognoz_data_in_DB():
        return '''
            SELECT * FROM prognoz
            WHERE period = %s AND category = %s;
            '''

    @staticmethod
    # Получить коэффициенты продаж по дням недели за период, выбранной категории
    def get_koeff_day_week_data_in_DB():
        return '''
            SELECT * FROM koeff_day_week
            WHERE period = %s AND category = %s;
            '''

    @staticmethod
    # Получить список кондитерских со всеми данными
    def get_dishe_in_DB():
        return '''
            SELECT * FROM dishes
            WHERE category_production = %s;
            '''

    @staticmethod
    # Получить количество строк в таблице dishes
    def get_rows_dishes():
        return '''
        SELECT COUNT(*) FROM dishes
        WHERE category_production = %s;
        '''