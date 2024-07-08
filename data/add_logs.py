import datetime
from data.server_requests import ServerRequests

server_requests = ServerRequests()
def add_log(log):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    data_server = server_requests.post('add_log', {"date": str(date), "time": str(time), "log": log})
    return data_server



