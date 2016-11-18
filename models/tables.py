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
                Field('user_id', 'reference auth_user', default=session.auth.user.id if session.auth else None),
                Field('cuisines'),
                Field('meal_type'),
                Field('name', 'string'),
                Field('description', 'text'),
                Field('ingredient', 'text'),
                Field('prept', 'time', default='00:00:00'),
                Field('cookt', 'time', default='00:00:00'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('vlink', 'text'),
                )

# Constraint for recipe
db.recipe.id.readable = db.recipe.id.writable = False
db.recipe.user_id.readable = db.recipe.user_id.writable = False
db.recipe.name.requires = IS_NOT_EMPTY()
db.recipe.created_on.writable = False
db.recipe.created_on.writable = False

db.recipe.cuisines.requires = IS_IN_SET(['Asian',
                                         'African',
                                         'European',
                                         'American',
                                         'Latin',
                                         'Indian',
                                         'Australian',
                                         'Polynesian'])

db.recipe.meal_type.requires = IS_IN_SET(['Breakfast & Brunch',
                                          'Lunch',
                                          'Dinner',
                                          'Deserts',
                                          'Appetizers',
                                          'Snacks'], multiple=True)



