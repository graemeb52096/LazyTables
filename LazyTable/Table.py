from LazyTable.Column import Column
from LazyTable.Fields import Integer, VarChar


class Table:
    """
    Mysql table
    """

    # Automatically creates id and date created columns
    id = Column('id', Integer(), primary_key=True)
    dateCreated = Column('dateCreated', VarChar(), required=True)

    def __init__(self, title):
        self.columns = []
        self.rows = []
        self.title = title
        self.add_column(self.id)
        self.add_column(self.dateCreated)

    def get_create_table_sql(self):
        statement = """CREATE TABLE %s (""" % self.title
        for col in self.columns:
            statement += "\n%s," % col[1].get_sql()
        statement = statement[:-1]
        statement += "\n);"
        return statement

    def add_column(self, col):
        self.columns.append((col.title, col))

    def add_columns(self, cols):
        for col in cols:
            self.columns.append((col, cols[col]))

    def add_row(self, row):
        self.rows.append(row)

    def has_column(self, col):
        for column in self.columns:
            if col == column[0]:
                return True
        return False

    def get_by_id(self, db, iid):
        cur = db.cursor()
        cur.execute("""SELECT * FROM %s WHERE id=%s""" % (
            self.title, iid
        ))
        rows = cur.fetchone()
        if rows == None:
            return {
                'error':
                'entry with id %s was not found in table %s' % (iid, self.title)
            }
        i = 0
        response = {}
        cols = self.get_cols()
        while i < len(rows):
            if cols[i].upper() == 'PASSWORD':
                response[cols[i]] = 'HIDDEN'
            else:
                response[cols[i]] = rows[i]
            i += 1
        return response

    def create_table(self, db):
        cur = db.cursor()
        cur.execute(self.get_create_table_sql())

    def get_cols(self):
        cols = []
        for col in self.columns:
            cols.append(col[0])
        return cols

    def get_rows(self):
        rows = []
        row = []
        for r in self.rows:
            for col in self.columns:
                row.append(r.values[col[0]])
            rows.append(row)
        return rows

    def generate_csv(self):
        cols = self.get_cols()
        rows = self.get_rows()
        output = ''
        for col in cols:
            output += '%s, ' % col
        output = output[:-2]
        output += '\n'
        for row in rows:
            for val in row:
                output += '%s, ' % val
            output = output[:-2]
            output += '\n'
        return output

    def compare(self, table):
        if len(self.columns) <= len(table.columns):
            for col in self.columns:
                if not table.has_column(col[0]):
                    return False
        else:
            pass
        return True

    def migration_additions(self, table):
        additions = []
        for column in table.columns:
            exists = False
            for col in self.columns:
                if col[0] == column[0]:
                    exists = True
            if not exists:
                additions.append((column[0], column[1]))
        return additions

    def migration_removals(self, table):
        removals = []
        for column in self.columns:
            exists = False
            for col in table.columns:
                if col[0] == column[0]:
                    exists = True
            if not exists:
                removals.append((column[0], column[1]))
        return removals

    def migrate(self, table):
        """
        Careful with this one
        """
        additions = self.migration_additions(table)
        removals = self.migration_removals(table)
        return additions, removals
