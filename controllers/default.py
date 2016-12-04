# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def test():
    recipes = db(db.recipe).select(orderby=~db.recipe.created_on, limitby=(0, 20))
    return dict(recipes=recipes)

def addRecipe():
    form = ''

    # check if user is login
    if auth.user:
        form = SQLFORM(db.recipe, labels={'mealType': 'Meal Type',
                                          'name': 'Name of Recipe',
                                          'prept': 'Prepare Time (minutes)',
                                          'cookt': 'Cooking Time (minutes)',
                                          'vURL': 'Youtube Video URL'})
        form.element(_id='recipe_name')['_placeholder'] = 'Name'
        form.element(_id='recipe_description')['_placeholder'] = 'Description'
        form.element(_id='recipe_ingredient')['_placeholder'] = 'Ingredient'
        form.element(_id='recipe_vURL')['_placeholder'] = 'https://www.youtube.com/watch?v='

        if form is not None and form.process().accepted:
            session.flash = T('Recipe Added')
            redirect(URL('default', 'index'))
        else:
            logger.info('Error!!')

    else:
        redirect(URL('default', 'user'))

    return dict(form=form)


def recipe():
    form = ''

    # check if user is login
    if auth.user:
        form = SQLFORM(db.recipe, labels={'mealType': 'Meal Type',
                                          'name': 'Name of Recipe',
                                          'prept': 'Prepare Time (minutes)',
                                          'cookt': 'Cooking Time (minutes)'
                                          })

        if form is not None and form.process().accepted:
            session.flash = T('Recipe Added')
            redirect(URL('default', 'index'))
        else:
            logger.info('Error!!')

    else:
        redirect(URL('default', 'user'))
    recipes = db(db.recipe).select(orderby=~db.recipe.created_on, limitby=(0, 4))
    return dict(form=form,
                recipes=recipes)


def index():
    cuisines = db(db.cuisines).select(db.cuisines.name)
    mealType = db(db.mealType).select(db.mealType.name)
    recipes = db(db.recipe).select(orderby=~db.recipe.created_on, limitby=(0, 4))
    return dict(cuisines=cuisines,
                mealType=mealType,
                recipes = recipes,
    )


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


