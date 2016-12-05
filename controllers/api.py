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

            po = dict(
                id=r.id,
                username=username,
                urecipe=urecipe,
                recipe_edit=False,
                created_on=r.created_on,
                updated_on=r.updated_on,
                user_email = r.user_email,
                name = r.name
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

