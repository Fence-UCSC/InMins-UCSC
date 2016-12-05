# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def mycookbook():
    cuisines = db(db.cuisines).select(db.cuisines.name)
    mealType = db(db.mealType).select(db.mealType.name)
    recipes = db(db.recipe).select(orderby=~db.recipe.created_on, limitby=(0, 4))
    recipe = db(db.recipe.id == request.args(0)).select().first()
    return dict(cuisines=cuisines,
                mealType=mealType,
                recipes=recipes,
                recipe=recipe,
                )
    #row=()
    #return dict(row=row)


def test():
    recipes = db(db.recipe).select(orderby=~db.recipe.created_on, limitby=(0, 20))
    return dict(recipes=recipes)

def recipeForm():
    form = None
    recipe = None
    page_type = None
    hasVideo = False;

    if request.args(0) is None:
        redirect(URL('default', 'recipeForm', args='add'))
    elif request.args(0) == 'add':
        if auth.user_id is None:
            redirect(URL('user', vars={'_next': URL('default', 'recipeForm', args='add')}))
            page_type = 'create'
        form = SQLFORM(db.recipe, labels={'mealType': 'Meal Type',
                                          'name': 'Name of Recipe',
                                          'prept': 'Prepare Time (minutes)',
                                          'cookt': 'Cooking Time (minutes)',
                                          'vURL': 'Youtube Video URL',
                                          'image': 'Recipe Image'})
        form.element(_id='recipe_name')['_placeholder'] = 'Name'
        form.element(_id='recipe_description')['_placeholder'] = 'Description'
        form.element(_id='recipe_ingredient')['_placeholder'] = 'Ingredient'
        form.element(_id='recipe_vURL')['_placeholder'] = 'https://www.youtube.com/watch?v='
    elif request.args(0) == 'edit':
        try:
            recipe = db(db.recipe.id == request.vars['rid']).select().first()
        except ValueError:
            session.flash = T('Invalid recipe id' + request.vars['rid'])
            redirect(URL('default', 'index'))
        if recipe is None:
            session.flash = T('Recipe does not exist')
            redirect(URL('default', 'recipeForm', args='add'))

        page_type = 'edit'

        form = SQLFORM(db.recipe, recipe, deletable=True, showid=False, labels={'mealType': 'Meal Type',
                                                                              'name': 'Name of Recipe',
                                                                              'prept': 'Prepare Time (minutes)',
                                                                              'cookt': 'Cooking Time (minutes)',
                                                                              'vURL': 'Youtube Video URL',
                                                                              'image': 'Recipe Image'})
        form.add_button(T('Cancel'), URL('default','recipe', args=recipe.id),_class='btn btn-warning')
    else:
        session.flash = T('Invalid URL')
        redirect(URL('default', 'index'))

    if form is not None and form.process().accepted:
        if page_type == 'create':
            session.flash = T('Recipe Added')
        elif page_type == 'edit':
            session.flash = T('Recipe Edited')
        redirect(URL('default', 'index'))


    return dict(form=form)


def recipe():
    recipe = None

    if request.args(0) is None:
        redirect(URL('default', 'recipeForm'))
    else:
        try:
            recipe = db(db.recipe.id == request.args(0)).select().first()
        except ValueError:
            session.flash = T('Invalid recipe id:' + request.args(0))
            redirect(URL('default', 'index'))
        if recipe is None:
            session.flash = T('Recipe id:' + request.args(0) + ' does not exist')
            redirect(URL('default', 'index'))

    return dict(recipe=recipe)


def index():
    cuisines = db(db.cuisines).select(db.cuisines.name)
    mealType = db(db.mealType).select(db.mealType.name)
    recipes = db(db.recipe).select(orderby=~db.recipe.created_on, limitby=(0, 4))
    recipe = db(db.recipe.id == request.args(0)).select().first()
    return dict(cuisines=cuisines,
                mealType=mealType,
                recipes = recipes,
                recipe=recipe,
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


