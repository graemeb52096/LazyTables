class Column:
    """
    Mysql Column
    """
    def __init__(self, title, value, required=False, unique=False,
                 primary_key=False, foreign_key_reference=None):
        """

        :param title: Column title
         :type title: str
        :param value: Column type(INTEGER, VarChar, etc)
         :type value: Object
        :param required: Is required?
         :type required bool
        :param unique: Is unique?
         :type unique: bool
        :param primary_key:
         :type primary_key: Is primary key?
        :param foreign_key_reference: What table column references
         :type foreign_key_reference: str
        """
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