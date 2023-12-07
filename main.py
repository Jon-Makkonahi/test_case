import json

from datetime import datetime


class Fora:
    # Инициализируем три словаря для удобного решения задачи
    def __init__(self):
        self.results_run = {}
        self.run_timedelta = {}
        self.participants = {}


    def __download_to_result_run(self):
        # Открываем файл
        file_txt = open(file='results_RUN.txt', mode='r', encoding='utf-8')
        while True:
            # Построчно проходимся по текстовому файлу записывая строки в память
            line = file_txt.readline().strip().replace(u'\ufeff', '')
            # Останавливаем цикл, если строки закончились
            if not line:
                break
            # Формируем словарь в формате "Номер": [старт, финиш]
            result = line.split(' ')
            if result[0] not in self.results_run.keys():
                self.results_run[result[0]] = [result[2]]
            else:
                self.results_run[result[0]].append(result[2])
        file_txt.close()
        return self.results_run
    

    def __counter_run_time(self):
        # В строка 36-39 происходит формирование нового словаря в виде 'номер': 'время результата'
        for key in (self.results_run.keys()):
            timedelta = datetime.strptime(self.results_run[key][1], '%H:%M:%S,%f') - datetime.strptime(self.results_run[key][0], '%H:%M:%S,%f')
            dt = datetime.strptime(str(timedelta), "%H:%M:%S.%f").time()
            self.run_timedelta[key] = (dt)
        # По строкам 41-42 отсортируем данный список
        sorted_tuples = sorted(self.run_timedelta.items(), key=lambda item: item[1])
        self.run_timedelta = {key: (values) for key, values in sorted_tuples}
        return self.run_timedelta

    # Данная функция используется для загрузки данных из JSON файла.
    def __download_json(self):
        with open(file='competitors2.json', mode='r', encoding='utf-8') as json_file:
            file_content = json_file.read()
            self.participants = json.loads(file_content)
        return self.participants

    # Функция выводит список результативности участников Марафона
    def __information_table_of_finalists(self):
        print('| Занятое место | Нагрудный номер | Имя | Фамилия | Результат |')
        print('| --- | --- | --- | --- | --- |')
        position = 1
        for key in self.run_timedelta.keys():
            print(f'| {position} | {key} | {self.participants[key]["Surname"]} | {self.participants[key]["Name"]} | {(self.run_timedelta[key].strftime("%H:%M:%S.%f")[3:11]).replace(".", ",")} |')
            position += 1

    # Функция вызова внутренних функций класса
    def main(self):
        self.__download_to_result_run()
        self.__counter_run_time()
        self.__download_json()
        self.__information_table_of_finalists()

    
if __name__ == '__main__':
    fora = Fora()
    fora.main()
