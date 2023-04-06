class Checks:

    @classmethod
    def is_complete(cls, text_data):
        return 'Trace complete' in text_data \
               or 'Трассировка завершена' in text_data

    @classmethod
    def is_timed_out(cls, text_data):
        return 'Request timed out' in text_data \
               or 'Превышен интервал ожидания' in text_data

    @classmethod
    def is_beginning(cls, text_data):
        return 'Tracing route' in text_data \
               or 'Трассировка маршрута' in text_data

    @classmethod
    def is_invalid_input(cls, text_data):
        return 'Unable to resolve' in text_data \
               or 'Не удается разрешить' in text_data
