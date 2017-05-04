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
        if values == None:
            return {'error': 'provided no values'}
        row = Model(table, values)
        insert_statement = row.get_insert_sql()
        cur = self.db.cursor()
        rv = cur.execute(insert_statement)
        id = self.db.insert_id()
        self.db.commit()
        return id

    def edit_row(self, table, id, values):
        pass

    def delete_row(self, table, id):
        cur = self.db.cursor()
        cur.execute("""DELETE FROM %s WHERE id=%s""" % (
            table, id
        ))
        self.db.commit()

    def select(self, table, columns, conditions=None):
        table = self.tables[table]
        statement = 'SELECT ('
        for col in columns:
            statement += '%s ,' % col
        statement = statement[:-2] + ')'
        statement = statement + 'FROM %s' % table.title
        cur = self.db.cursor()
        cur.execute(statement)
        rows = cur.fetchall()
        response = {}
        for row in rows:
            i = 0
            while i < len(columns):
                response[columns[i]] = row[i]
                i += 1
        return response

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
                    print('Did not removed column: ', removal[0])
            else:
                schema = self.tables[table].get_create_table_sql()
                cur.execute(schema)
                print('Added table %s' % table)
