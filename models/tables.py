# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('categories',
                Field('name', 'string'),
                Field('description', 'string')
                )

db.define_table('recipe',
                Field('user_id', 'reference auth_user', default=session.suth.user.id if session.auth else None),
                Field('username', default=session.auth.user.first_name if session.auth else None),
                Field('eating_style'),
                Field('meal_type'),
                Field('name', 'string'),
                Field('description', 'string'),
                Field('prep', 'time'),
                Field('cook', 'time'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('vlink', 'text', default=None)
                )

db.define_table('ingredient',
                Field('recipe_id', 'reference recipe', requires=IS_IN_DB(db, 'recipe.id')),
                Field('material', 'text'),
                Field('amount', 'double'),
                Field('unit', 'string')
                )

# recipe table's constraint
db.recipe.user_id.readable = db.recipe.user_id.writable = False
db.recipe.username.readable = db.recipe.username.writable = False
db.recipe.eating_style.requires = IS_IN_SET('Omnivore', 'Vegetarian', 'Vegan')
db.recipe.meal_type.requires = IS_IN_SET('Appetizers & Snacks',
                                         'Breakfast & Brunch',
                                         'Lunch & Dinner',
                                         'Dessert',
                                         'Drinks')
db.recipe.name.requires = IS_NOT_EMPTY()
db.recipe.created_on.readable = db.recipe.created_on.writable = False
db.recipe.updated_on.readable = db.recipe.updated_on.writable = False

