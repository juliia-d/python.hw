class Time:
    def __init__(self, minutes = 5, seconds = 30):
        self.minutes = minutes
        self.seconds = seconds
    def __str__(self):
        return f'Час: {self.minutes} хв. {self.seconds} c.'
    def total_seconds(self):
        return self.minutes*60 + self.seconds
    def __add__(self, seconds = 32):
        total_sec = self.total_seconds() + seconds
        return Time(total_sec // 60, total_sec % 60)
class Runner(Time):
    def __init__(self, minutes = 5, seconds = 30, surname = 'Ковальчук', distance_km = 1):
        Time.__init__(self, minutes, seconds)
        self.surname = surname
        self.distance_km = distance_km
    def speed(self):
        hours = self.total_seconds() / 3600
        return self.distance_km / hours if hours > 0 else 0
    def __lt__(self, other):
        return self.speed()  < other.speed()
    def __str__(self):
        return f'{self.surname}: {self.distance_km} км за {Time.__str__(self)} (швидкість {self.speed():.2f} км/год)'
class Results:
    def __init__(self):
        self.runners = []
    def add_runner(self, runner: Runner):
        self.runners.append(runner)
    def add_from_file(self, results):
        file = open(results, 'r', encoding='utf-8')  
        for line in file:
            parts = line.strip().split(',') 
            if len(parts) == 4:
                minutes = int(parts[0])  
                seconds = int(parts[1])
                surname = parts[2]
                distance = float(parts[3]) 

                self.runners.append(Runner(minutes, seconds, surname, distance))

        file.close()
    
    def show_slowest_runners(self, n):
        slowest_runners = []
        for i in range(n):
            slowest = min(self.runners)
            slowest_runners.append(slowest)
            self.runners.remove(slowest)
        for runner in slowest_runners:
            print(runner)

        
    
if __name__ == '__main__':
    t1 = Time()
    print(t1)
    t2 = t1 + 32
    print(t2)

    runner1 = Runner(5, 30, 'Ковальчук', 1)
    runner2 = Runner(4, 58, 'Лебідь', 1)
    runner3 = Runner(5, 42, 'Швець', 1)

    results = Results()
    results.add_runner(runner1)
    results.add_runner(runner2)
    results.add_runner(runner3)
    print('Топ-2 найповільніших бігуни:')
    results.show_slowest_runners(2)
