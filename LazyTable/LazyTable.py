from LazyTable.Column import Column
from LazyTable.Fields import Integer, VarChar
from LazyTable.Model import Model
from LazyTable.Table import Table


class LazyTable(Table):
    """
    Lazy Table allows quick table developments
    using dictionaries and tuples.


    username_type = 'str'
    username_parameters = 'required/unique/n'
    user_columns = {}
    user_columns['username'] = (username_type, username_parameters)

    Note: Parameter string must be empty or
    At the end of a parameter string specify
    foreign key table reference or use '/n'
    for none

    Lazy Syntax example:
        user_columns = {
            'username': ('str', 'required/unique/n'),
            'password': ('str', 'required/n'),
            'email': ('str', 'unique/required/n'),
            'firstName': ('str', 'required/n'),
            'lastName': ('str', 'required/n'),
            'location': ('str', '')
        }
        user_table = LazyTable('User', user_columns)
    """
    def __init__(self, title, cols):
        super().__init__(title)
        for col in cols:
            if cols[col][0] == 'int':
                val = Integer()
            elif cols[col][0] == 'str':
                val = VarChar()
            if cols[col][1] == '':
                self.add_column(Column(col, val))
            else:
                options = cols[col][1]
                options = options.split('/')
                if 'required' in options:
                    required = True
                else:
                    required = False
                if 'unique' in options:
                    unique = True
                else:
                    unique = False
                if 'primary_key' in options:
                    primary_key = True
                else:
                    primary_key = False
                if options[-1] == 'n':
                    self.add_column(Column(
                        col, val, required=required,
                        unique=unique, primary_key=primary_key
                    ))
                else:
                    self.add_column(Column(
                        col, val, required=required,
                        unique=unique, primary_key=primary_key,
                        foreign_key_reference=options[-1]
                    ))

    def GET(self, db, iid):
        self.get_by_id(db, iid)

    def POST(self, db, vals):
        row = Model(self, vals)
        self.add_row(row)
        row.insert_row()

    def PUT(self, vals):
        row = Model(self, vals)
        pass

    def DELETE(self, iid):
        pass
