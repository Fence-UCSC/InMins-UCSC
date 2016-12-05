# These are the controllers for your ajax api.


def get_user_name_from_id(uid):
    u = db(db.auth_user.id == uid).select().first()
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
            uname = get_user_name_from_id(r.user_id)
            img_str = json.dumps(r.image)
            has_image = True if (img_str != "\"\"") else False
            image = URL('appadmin', 'download/db', args=r.image)
            recipe_url = URL('default', 'recipe', args=r.id)

            recipe = dict(
                id=r.id,
                username=uname,
                recipe_name=r.name,
                recipe_image=image,
                had_image=has_image,
                created_on=r.created_on,
                recipe_url=recipe_url
            )
            recipes.append(recipe)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        recipes=recipes,
        has_more=has_more,
        logged_in=logged_in
    ))

