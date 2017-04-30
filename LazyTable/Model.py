import datetime
import json


class Model:
    """
    Basic row model

    Values are stored in dictionary
    """
    def __init__(self, table, values):
        self.table = table
        self.values = values
        self.values['dateCreated'] = datetime.datetime.now()

    def get_cols(self):
        cols = '('
        for val in self.values:
            cols += '%s, ' % val
        cols = cols[:-2]
        cols += ')'
        return cols

    def get_insert_sql(self):
        cols = self.get_cols()
        statement = """INSERT INTO %s %s VALUES(""" % (
            self.table.title, cols
        )
        for val in self.values:
            if type(self.values[val]) == int:
                statement += '%s, ' % self.values[val]
            else:
                statement += "'%s', " % self.values[val]
        statement = statement[:-2]
        statement += ");"
        return statement

    def get_json(self):
        return json.dumps(self.values)

    def insert_row(self, db):
        cur = db.cursor()
        cur.execute(self.get_insert_sql())
