class DataVector:
    # класс возвращает данные для таблицы как вектор
    @classmethod
    def get_args(cls, count, info):
        print(info)
        try:
            as_number = info['org'].split()[0][2::]
            provider = " ".join(info['org'].split()[1::])
        except KeyError:
            as_number, provider = '*', '*'
        return [f"{count}.", info['ip'], info['country'], as_number, provider]

    @classmethod
    def get_bogon_args(cls, count, info):
        return [f"{count}.", info['ip'], '*', '*', '*']
