import pickle 
import shelve
import json


class RunnerError(Exception):
    pass

class InvalidTimeError(Exception):
    """Клас винятку для некоректного часу"""
    pass


class Time:
    def __init__(self, minutes = 5, seconds = 30):
        if not isinstance(minutes, int) or not isinstance(seconds, int):
            raise InvalidTimeError("Час має бути цілим числом")
        if minutes < 0 or seconds < 0:
            raise InvalidTimeError("Час не може бути від'ємним!")
        self.minutes = minutes
        self.seconds = seconds

    def __str__(self):
        return f'Час: {self.minutes} хв. {self.seconds} c.'

    def total_seconds(self):
        return self.minutes * 60 + self.seconds

    def __add__(self, seconds = 32):
        total_sec = self.total_seconds() + seconds
        return Time(total_sec // 60, total_sec % 60)

class Runner(Time):
    def __init__(self, minutes = 5, seconds = 30, surname = 'Ковальчук', distance_km = 1):
        Time.__init__(self, minutes, seconds)
        self.surname = surname
        self.distance_km = distance_km
        assert self.distance_km > 0, "Дистанція повинна бути більшою за 0"

    def speed(self):
        hours = self.total_seconds() / 3600
        return self.distance_km / hours if hours > 0 else 0

    def __lt__(self, other):
        return self.speed()  < other.speed()

    def __str__(self):
        return f'{self.surname}: {self.distance_km} км за {super().__str__()} (швидкість {self.speed():.2f} км/год)'

class Results:
    def __init__(self):
        self.runners = []

    def add_runner(self, runner: Runner):
        self.runners.append(runner)

    def add_from_file(self, results):
        try:
            with open(results, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        raise RunnerError("Неправильний формат рядка у файлі.")
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    surname = parts[2]
                    distance = float(parts[3])
                    self.add_runner(Runner(minutes, seconds, surname, distance))
        except FileNotFoundError:
            print("[Помилка]: Файл не знайдено.")
        except ValueError:
            print("[Помилка]: Невірні типи даних у файлі.")
        except RunnerError as e:
            print(f"[RunnerError]: {e}")
        else:
            print("Дані з файлу успішно додано.")
        finally:
            print("Зчитування з файлу завершено.")
    def show_slowest_runners(self, n):
        slowest_runners = []
        for _ in range(min(n, len(self.runners))):
            slowest = min(self.runners)
            slowest_runners.append(slowest)
            self.runners.remove(slowest)
        for runner in slowest_runners:
            print(runner)

    def save_pickle(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.runners, f)

    def load_pickle(self, filename):
        with open(filename, 'rb') as f:
            self.runners = pickle.load(f)

    def save_shelve(self, filename):
        with shelve.open(filename) as db:
            db['runners'] = self.runners

    def load_shelve(self, filename):
        with shelve.open(filename) as db:
            self.runners = db.get('runners', [])

    def save_repr(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str([f"Runner({r.minutes}, {r.seconds}, '{r.surname}', {r.distance_km})" for r in self.runners]))

    def load_repr(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = eval(f.read())  
            self.runners = [eval(r) for r in data]

    def save_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([runner.__dict__ for runner in self.runners], f, ensure_ascii=False, indent=4)

    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.runners = [Runner(**data) for data in json.load(f)]


if __name__ == '__main__':
    try:
        t1 = Time()
        print(t1)
        t2 = t1 + 32
        print(t2)

        results = Results()

        count = int(input("Скільки бігунів ви хочете ввести? "))
        for i in range(count):
            print(f"\nВведення даних для бігуна №{i+1}")
            try:
                minutes = int(input("  Хвилини: "))
                if minutes < 0:
                    raise InvalidTimeError("Хвилини не можуть бути від'ємними!")
                seconds = int(input("  Секунди: "))
                if seconds < 0:
                    raise InvalidTimeError("Секунди не можуть бути від'ємними!")
            except InvalidTimeError as e:
                print(f"[Критична помилка]: {e}")
                continue

            surname = input("  Прізвище: ")
            distance = float(input("  Дистанція (км): "))
            runner = Runner(minutes, seconds, surname, distance)
            results.add_runner(runner)
            print("  Бігуна успішно додано.")

        print('\nТоп-2 найповільніших бігуни:')
        results.show_slowest_runners(2)

        results.save_pickle('runners.pkl')
        results.save_shelve('runners_shelve')
        results.save_repr('runners_repr.txt')
        results.save_json('runners.json')

        results.load_pickle('runners.pkl')
        results.load_shelve('runners_shelve')
        results.load_repr('runners_repr.txt')
        results.load_json('runners.json')

    except (RunnerError, InvalidTimeError) as e:
        print(f"[Критична помилка]: {e}")
    except Exception as e:
        print(f"[Невідома помилка]: {e}")
    finally:
        print("Завершення виконання скрипта.")
