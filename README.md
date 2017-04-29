## Currently Supports
 -Mysql

## Basic usage
    db = MySQLdb.connect("localhost", "root", "", "database")
    registry = LazyRegister(db)
    registry.render()
    columns = {
      'username': ('str', 'unique/required/n',
      'password': ('str', 'required/n')
    }
    registry.push('User', columns)
    registry.update()

## Description
LazyTable was created to make mysql a lot more... **LAZY**

Not every feature desired for the final LazyTable is complete.

LazyTable hopes to tackle schema design, as well as
handle table updates and changes so that we
can be lazy.

## Lazy Table
LazyTable takes two parameters to start,
a title and a dictionary that represents
our columns.

    table = LazyTable("User", {'username': ('str','')})

A column can be a string or int, can be
required, unique, primary_key, or have
a foreign key reference.

Column parameters can be empty:

    col_type = 'int'
    col_params = ''

 Or can define one configs:

    col_type = 'str'
    col_params = 'unique/n'

 Or can define multiple configs

    col_type = 'int'
    col_params = 'required/unique/User'

 **Note that if we define any configurations,
 we must provide a foreign key reference at
 the end of config statement. Use "/n" for none.**

## Basic Example
    username_col_type = 'str'
    username_col_parameters = 'required/unique/n'
    password_col_type = 'str'
    password_col_parameters = 'required/n
    user_columns = {}
    user_columns['username'] = (username_col_type, username_col_parameters)
    user_columns['password'] = (password_col_type, password_col_parameters)
    user_table = LazyTable('User', user_columns)

## Lazy Example
    user_columns = {
        'username': ('str', 'required/unique/n'),
        'password': ('str', 'required/n'),
        'email': ('str', 'unique/required/n'),
        'firstName': ('str', 'required/n'),
        'lastName': ('str', 'required/n'),
        'location': ('str', '')
    }
    post_columns = {
        'uid': ('int', 'required/User'),
        'title': ('str', ''),
        'media': ('str', ''),
        'description': ('str', ''),
        'upVotes': ('int', '')
    }
    user_table = LazyTable('User', user_columns)
    post_table = LazyTable('Post', post_columns)

# LazyRegister
## Description
Registers can be used to manage a database,
and migrate tables.

    LazyRegister.register(table)
Will add table to registry

    LazyRegister.push('Title', columns)
Will create a new table and add to registry

    LazyReigister.render()
Will pull current database tables, and load
them to register

    LazyRegister.update()
Will update database with any changes made
as well as add any tables from registry not currently
in the database


## Example
    db = MySQLdb.connect("localhost", "root", "", "database")
    registry = Register(db)
    registry.render()
    registry.register(user_table)
    reigstry.update()

## Lazy Example
    db = MySQLdb.connect("localhost", "root", "", "database")
    registry = LazyRegister(db)
    registry.render()
    registry.push('User', user_columns)
    registry.update()
