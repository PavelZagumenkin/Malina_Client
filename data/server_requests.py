import requests

class ServerRequests:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url

    def post(self, endpoint, json_data=None):
        try:
            response = requests.post(f'{self.base_url}/{endpoint}', json=json_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {'result': 'Критическая ошибка: Сервер не доступен!'}
        except requests.exceptions.HTTPError as err:
            return {'result': f'Критическая ошибка: HTTP ошибка: {err}!'}
        except requests.exceptions.RequestException as err:
            return {'result': f'Критическая ошибка: Ошибка запроса: {err}!'}