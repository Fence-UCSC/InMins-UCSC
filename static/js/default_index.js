// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    function get_recipes_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return recipes_url + "?" + $.param(pp);
    }

    self.add_recipe_button = function () {
        $("#newrecipe").addClass('hidden');
        self.vue.is_adding_recipe = true;
        self.vue.recipe_content = '';
    };

    self.delete_recipe = function (recipe_id, user_email) {
        $.recipe(del_recipe_url,
            {
                recipe_id: recipe_id,
                user_email: user_email
            },
            function (data) {
                if (data.isDeleted) {
                    var idx = null;
                    for (var i=0; i<self.vue.recipes.length; i++) {
                        if (self.vue.recipes[i].id === recipe_id) {
                            idx = i +1;
                            break;
                        }
                    }
                    if (idx) {
                        self.vue.recipes.splice(idx-1, 1);
                    }
                }
            })
    };

    self.cancel_recipe_button = function () {
        self.vue.is_adding_recipe = false;
        $("#newrecipe").removeClass('hidden');
    };

    self.get_recipes = function () {
        $.getJSON(get_recipes_url(0,4), function (data) {
            self.vue.recipes = data.recipes;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        })
    };

    self.add_recipe = function () {
      console.log("add_recipe is called");
      $.recipe(add_recipe_url,
          {
              recipe_content: self.vue.recipe_content
          },
          function (data) {
              self.vue.recipes.unshift(data.recipe);
          });
       self.cancel_recipe_button();
    };


    self.get_more = function () {
        var num_recipes = self.vue.recipes.length;
        $.getJSON(get_recipes_url(num_recipes, num_recipes + 4), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.recipes, data.recipes);
        });
    };



    self.update_recipe = function (recipe) {
        console.log("update_recipe is called");
        $.recipe(update_recipe_url,
            {
                new_recipe_content: self.vue.recipe_edit_content,
                recipe_id: recipe.id
            },
            function (data) {
                for (var i=0; i<self.vue.recipes.length; i++) {
                    if (self.vue.recipes[i].id == data.recipe_id) {
                        self.vue.recipes[i].recipe_content = data.recipe_content;
                        self.vue.recipes[i].updated_on = data.updated_on;
                    }
                }
            }
        );
        recipe.recipe_edit = false;
    };

     self.edit_recipe = function (recipe) {
        recipe.recipe_edit = true;
        self.vue.recipe_edit_content = recipe.recipe_content;
    };

    self.cancel_editing = function (recipe) {
        recipe.recipe_edit = false;
    };


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            has_more: false,
            logged_in: true,
            is_adding_recipe: false,
            recipes: [],
            recipe_content: null,
            recipe_edit_content: null
        },
        methods: {
            add_recipe_button: self.add_recipe_button,
            cancel_recipe_button: self.cancel_recipe_button,
            get_more: self.get_more,
            add_recipe: self.add_recipe,
            delete_recipe: self.delete_recipe,
            edit_recipe: self.edit_recipe,
            cancel_editing: self.cancel_editing,
            update_recipe: self.update_recipe
        }

    });

    self.get_recipes();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
