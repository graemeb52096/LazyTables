from LazyTable.Register import Register
from LazyTable.LazyTable import LazyTable
from LazyTable.Model import Model


class LazyRegister(Register):
    """
    Lazy Register adds push and update function
    push Register.
    """
    def push(self, title, cols):
        """
        Creates and registers a table
        """
        table = LazyTable(title, cols)
        self.register(table)

    def add_tables(self):
        for tab in self.tables:
            self.tables[tab].create_table(self.db)

    def insert_row(self, table, values):
        row = Model(table, values)
        insert_statement = row.get_insert_sql()
        cur = self.db.cursor()
        cur.execute(insert_statement)
        self.db.commit()

    def edit_row(self, table, values):
        pass

    def delete_row(self, table, id):
        pass


    def update(self):
        """
        Checks registry for changes not present in
        database and updates accordingly
        """
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
