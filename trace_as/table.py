from prettytable import PrettyTable


class TableManager:
    @classmethod
    def generate_table(cls):
        table = PrettyTable()
        table.field_names = ["number", "ip", "country", "AS number", "provider"]
        return table
