# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('recipe',
                Field('user_id', 'reference auth_user', default=session.suth.user.id if session.auth else None),
                Field('username', default=session.auth.user.first_name if session.auth else None),
                Field('name', 'string'),
                Field('description', 'string'),

                Field('prep', 'time'),
                Field('cook', 'time'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('vlink', 'text', default=None)
                )

db.define_table('ingredients',
                Field('recipe_id', 'reference recipe', requires=IS_IN_DB(db, 'recipe.id')),
                Field('material', 'text')
                )

# the constraint of recipe table
db.recipe.name.requires = IS_NOT_EMPTY()

