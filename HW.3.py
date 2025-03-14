class Time:
    def __init__(self, minutes: int, seconds: int):
        self.minutes = minutes
        self.seconds = seconds
    def __str__(self):
        return f'Time[{self.minutes} хв. {self.seconds} c.]'
    def total_seconds(self):
        return self.minutes*60 + self.seconds
    def __add__(self, seconds: int):
        total_sec = self.total_seconds() + seconds
        return Time(total_sec // 60, total_sec % 60)

t1 = Time(5, 30)
print(t1)
t2 = t1 + 32
print(t2)
