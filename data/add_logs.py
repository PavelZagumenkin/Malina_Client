import datetime
import requests


def add_log(log):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    try:
        response = requests.post('http://localhost:5000/add_log', json={"date": str(date), "time": str(time), "log": log})
        response.raise_for_status()  # Проверка, успешен ли запрос
        data = response.json()
        result = data['result']
    except requests.exceptions.ConnectionError:
        result = 'Сервер не доступен!'
    except requests.exceptions.HTTPError as err:
        result = f'HTTP ошибка: {err}'
    except requests.exceptions.RequestException as err:
        result = f'Ошибка запроса: {err}'
    return result



