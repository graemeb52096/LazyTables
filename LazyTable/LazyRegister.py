from LazyTable.Register import Register
from LazyTable.LazyTable import LazyTable


class LazyRegister(Register):
    def push(self, title, cols):
        table = LazyTable(title, cols)
        self.register(table)

    def add_tables(self):
        for tab in self.tables:
            self.tables[tab].create_table(self.db)

    def update(self):
        current = LazyRegister(self.db)
        current.render()
        cur = self.db.cursor()
        for table in self.tables:
            if table in current.tables:
                additions, removals = current.tables[table].migrate(self.tables[table])
                for addition in additions:
                    cur.execute("""ALTER TABLE %s ADD COLUMN %s""" % (
                        table, addition[1].get_sql()
                    ))
                    print('Added column: ', addition[0])
                for removal in removals:
                    #cur.execute("""ALTER TABLE %s DROP COLUMN %s""" % (
                    #    table, removal[0]
                    #))
                    #print('Removed column: ', removal[0])
                    print("Didnt removed column: ", removal[0])
            else:
                schema = self.tables[table].get_create_table_sql()
                cur.execute(schema)
                print('Added table %s' % table)
