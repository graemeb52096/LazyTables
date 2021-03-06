from LazyTable.Table import Table
from LazyTable.LazyTable import LazyTable
from LazyTable.Column import Column


class Register():
    """
    Basic registry.
    Stores db table info and Generates Schemas
    """
    def __init__(self, db):
        self.db = db
        self.tables = {}

    def register(self, table):
        if table in self.tables:
            if self.tables[table.title].compare(table):
                self.tables[table.title] = table
            else:
                add, rem = self.tables[table.title].migrate(table)
                print (
                    "Not safe to overwrite this table... use force_register()"
                )
                print (
                    "Changes:\n%s\n%s" % (add, rem)
                )
        else:
            self.tables[table.title] = table

    def force_register(self, table):
        self.tables[table.title] = table

    def fetch(self, table, iid):
        return self.tables[table].get_by_id(self.db, iid)

    def fetch_column(self, table, column, iid):
        if table.has_column(column):
            cur = self.db.cursor()
            cur.execute("""SELECT %s FROM %s WHERE id=%s""" %(
                column, table.title, iid
            ))
        else:
            print("Column does not exist check spelling.")

    def generate_schema(self):
        schema = ""
        for tab in self.tables:
            schema += (self.tables[tab].get_create_table_sql())
            schema += '\n'
        return schema

    def compare(self, registry):
        for table in self.tables:
            for tab in registry.tables:
                if self.tables[table] == registry.tables[tab]:
                    self.tables[table].compare(registry.tables[tab])

    def get_tables_from_db(self):
        cur = self.db.cursor()
        cur.execute("SHOW TABLES")
        return cur.fetchall()

    def handle_foreign_key_schema(self, col, design):
        index = (col.find('FOREIGN KEY'))
        index += 12
        col = col[index:-7]
        col_name = (col.split("REFERENCES")[0])[2:-3]
        reference = col.split("REFERENCES")[1].strip()
        reference = reference[1:-1]
        param_string = design[col_name][1]
        param_string = param_string[:-1] + reference
        return col_name, param_string

    def schema_to_table(self, table):
        cur = self.db.cursor()
        cur.execute("SHOW CREATE TABLE %s" % table)
        sql = cur.fetchone()
        for cols in sql:
            sql = cols
        sql = sql.split('\n')
        i = 1
        design = {}
        while i < (len(sql) - 1):
            col = sql[i]
            col = col.strip()
            if "PRIMARY KEY" in col:
                pass
            elif "FOREIGN KEY" in col:
                col_name, params = self.handle_foreign_key_schema(col, design)
                kind = design[col_name][0]
                design[col_name] = (kind, params)
            elif "UNIQUE KEY" in col:
                col = col[10:]
                col = col.strip()
                col = col.split('`')
                col_name = col[1]
                col_kind = design[col_name][0]
                col_params = design[col_name][1]
                col_params = 'unique/' + col_params
                design[col_name] = (col_kind, col_params)
            else:
                title = col.split("`")[1]
                if title != 'id' and title != 'dateCreated':
                    param_string = ''
                    if "int" in col:
                        kind = 'int'
                    else:
                        kind = 'str'
                    if "NOT NULL" in col:
                        param_string += 'required/'
                        required = True
                    if param_string != '':
                        param_string += 'n'
                    design[title] = (kind, param_string)
            i += 1
        return LazyTable(table, design)

    def render(self):
        '''
        Loads tables schemas from database
        '''
        table_list = self.get_tables_from_db()
        for table_name in table_list:
            if table_name is not None:
                table_name = table_name[0]
                table = self.schema_to_table(table_name)
                self.register(table)
