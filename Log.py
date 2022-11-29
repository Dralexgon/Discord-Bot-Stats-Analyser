from datetime import datetime

class Log:

    @staticmethod
    def print(message : str):
        print(f"[{datetime.now().strftime('%Y/%m/%d|%H:%M:%S')}]: {message}")