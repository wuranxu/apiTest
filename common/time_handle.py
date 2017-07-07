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

    @classmethod
    def now_str(self):
        return self.now().strftime(self.time_format)

    @classmethod
    def delta(self, start, end):
        return (self.time_dt(end) - self.time_dt(start)).total_seconds()