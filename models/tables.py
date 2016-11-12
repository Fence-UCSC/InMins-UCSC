# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('checklist',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('title'),
                Field('checklist', 'text'),
                Field('last_opened', 'datetime', update=datetime.datetime.utcnow())
                )

# I don't want to display the user email by default in all forms.
db.checklist.id.readable = db.checklist.id.writable = False
db.checklist.user_email.readable = db.checklist.user_email.writable = False
db.checklist.last_opened.readable = db.checklist.last_opened.writable = False
db.checklist.title.requires = IS_NOT_EMPTY()

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
