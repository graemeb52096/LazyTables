# Detailed example:

    >>> username_col = Column('username', VarChar(), unique=True, required=True)
    >>> password_col = Column('password', VarChar(), required=True)
    >>> user_table = Table('User')
    >>> user_table.add_column(username_col)
    >>> user_table.add_column(password_col)
    >>> db = MySQLdb.connect("localhost", "root", "password", "database")
    >>> registry = Register(db)
    >>> registry.register(user_table)
    >>> registry.generate_schema()
    CREATE TABLE User (
    id NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(id),
    dateCreated NOT NULL,
    username UNIQUE NOT NULL,
    password NOT NULL
    )
    
# Lazy Example:

    >>> user = {'username': ('str', 'required/unique/n'), 'password': 'required/n')}
    >>> db = MySQLdb.connect("localhost", "root", "password", "database")
    >>> registry = LazyRegister(db)
    >>> registry.push('User', user)
    >>> registry.generate_schema()
    CREATE TABLE User (
    id NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(id),
    dateCreated NOT NULL,
    username UNIQUE NOT NULL,
    password NOT NULL
    )
    

# Class breakdown
## Fields

Lazy table so far provides the following Field types:
 
  -Integer
  
  -VarChar

### Integer

    class Integer:
      """
      Represents INTEGER type for mysql columns
      """
      def __init__(self, kind="INT"):
          self.kind = kind

      def __str__(self):
          return self.kind

      def __repr__(self):
          return "%s" % self.kind

### VarChar

    class VarChar:
        """
        Represents VARCHAR type for mysql columns
        """
        def __init__(self, length=64):
            self.length = length

        def __str__(self):
            return """VARCHAR(%s)""" % self.length

        def __repr__(self):
            return """VARCHAR(%s)""" % self.length
            

## Column

Columns take a minimum of two arguments, title and
value type.


        class Column:
        """
        Column accepts a title, a value type as well as
        a slew of optional parameters to define your column
        """
            def __init__(self, title, value, required=False, unique=False,
                 primary_key=False, foreign_key_reference=None):
                self.title = title
                self.value = value
                self.required = required
                self.unique = unique
                self.primary_key = primary_key
                self.foreign_key_reference = foreign_key_reference

            def get_sql(self):
                statement = """%s %s""" % (self.title, str(self.value))
                if self.primary_key:
                    statement += " AUTO_INCREMENT"
                if self.required:
                    statement += " NOT NULL"
                if self.unique:
                    statement += ",\nUNIQUE KEY `%s` (`%s`)" % (self.title, self.title)
                if self.primary_key:
                    statement += ",\nPRIMARY KEY (%s)" % self.title
                if self.foreign_key_reference:
                    statement += ",\nFOREIGN KEY (%s) REFERENCES %s(id)" % (
                        self.title, self.foreign_key_reference
                   )
            return statement
        
            def compare(self):
                pass
                
## Table
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
            print ("Table: %s id: %s" % (self.title, iid))
            cur.execute("""SELECT * FROM %s WHERE id=%s""" % (
                self.title, iid
            ))
            rows = cur.fetchone()
            i = 0
            response = {}
            cols = self.get_cols()
            while i < len(rows):
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

