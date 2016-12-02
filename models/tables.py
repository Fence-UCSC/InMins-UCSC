# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime
db.define_table('cuisines',
                Field('name'))

db.define_table('mealType',
                Field('name'))

# insert data cuisines table
if db(db.cuisines.id > 0).isempty():
    db.cuisines.insert(name='African')
    db.cuisines.insert(name='American')
    db.cuisines.insert(name='Asian')
    db.cuisines.insert(name='Australian')
    db.cuisines.insert(name='European')
    db.cuisines.insert(name='Indian')
    db.cuisines.insert(name='Latin')
    db.cuisines.insert(name='Polynesian')

# insert data to mealType table
if db(db.mealType.id > 0).isempty():
    db.mealType.insert(name='Breakfast & Brunch')
    db.mealType.insert(name='Lunch')
    db.mealType.insert(name='Dinner')
    db.mealType.insert(name='Desserts')
    db.mealType.insert(name='Appetizers')
    db.mealType.insert(name='Snacks')

db.define_table('recipe',
                Field('user_id', 'reference auth_user', default=session.auth.user.id if session.auth else None),
                Field('cuisines'),
                Field('mealType'),
                Field('name', 'string'),
                Field('description', 'text'),
                Field('ingredient', 'text'),
                Field('prept', 'integer', default=0),
                Field('cookt', 'integer', default=0),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('vlink', 'text'),
                Field('status', 'boolean', default=True),
                Field('username', default=session.auth.user.first_name if session.auth else None),
                )

# Constraint for recipe
db.recipe.name.requires = IS_NOT_EMPTY()
db.recipe.cuisines.requires = IS_IN_DB(db, 'cuisines', '%(name)s')
db.recipe.mealType.requires = IS_IN_DB(db, 'mealType', '%(name)s')
db.recipe.id.readable = db.recipe.id.writable = False
db.recipe.user_id.readable = db.recipe.user_id.writable = False
db.recipe.created_on.writable = db.recipe.created_on.readable = False
db.recipe.updated_on.writable = db.recipe.updated_on.readable = False
db.recipe.vlink.writable = db.recipe.vlink.readable = False


