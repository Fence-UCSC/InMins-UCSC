# These are the controllers for your ajax api.


def get_user_name_from_email(email):
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def get_recipes():

    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0

    recipes = []
    has_more = False
    rows = db().select(db.recipe.ALL, orderby=~db.recipe.created_on, limitby=(start_idx, end_idx + 1))

    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            username = get_user_name_from_email(r.user_email)
            if auth.user:
                urecipe = True if auth.user.email == r.user_email else False
            else:
                urecipe = False

            po = dict(
                id=r.id,
                username=username,
                urecipe=urecipe,
                recipe_edit=False,
                created_on=r.created_on,
                updated_on=r.updated_on,
                user_email = r.user_email,
                recipe_content = r.recipe_content
            )
            recipes.append(po)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        recipes=recipes,
        has_more=has_more,
        logged_in=logged_in
    ))


# Note that we need the URL to be signed, as this changes the db.
@auth.requires_signature()
def add_recipe():

    po_id = db.recipe.insert(
        recipe_content=request.vars.recipe_content
    )

    po = db.recipe(po_id)
    username = get_user_name_from_email(po.user_email)
    if auth.user:
        urecipe = True if auth.user.email == po.user_email else False
    else:
        urecipe = False
        urecipe = False

    recipe = dict(
        id=po.id,
        username=username,
        urecipe=urecipe,
        created_on=po.created_on,
        updated_on=po.updated_on,
        user_email=po.user_email,
        recipe_content=po.recipe_content
    )

    return response.json(dict(recipe=recipe))


@auth.requires_signature()
def del_recipe():
    if (auth.user.email == request.vars.user_email):
        db(db.recipe.id == request.vars.recipe_id).delete()
        isDeleted = True
    else:
        session.flash = T('Not Authorized')
        isDeleted = False
    return response.json(dict(isDeleted=isDeleted))


@auth.requires_signature()
def update_recipe():
    recipe_id = request.vars.recipe_id
    recipe_content = request.vars.new_recipe_content

    db(db.recipe.id == recipe_id).update(
        recipe_content=recipe_content,
        updated_on=datetime.datetime.utcnow())

    recipe = db(db.recipe.id == recipe_id).select().first()

    return response.json(dict(
        recipe_id=recipe.id,
        recipe_content=recipe.recipe_content,
        updated_on=recipe.updated_on
    ))
