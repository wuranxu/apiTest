__author__ = 'Woody'
from datetime import datetime
from initial import app


class handle():
    time_format = app.config['TIMEFORMAT']

    @classmethod
    def time_str(self, dt):
        return dt.strftime(self.time_format)

    @classmethod
    def time_dt(self, string):
        return datetime.strptime(string, self.time_format)

    @classmethod
    def now(self):
        return datetime.now()