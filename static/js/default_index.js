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


    self.get_recipes = function () {
        $.getJSON(get_recipes_url(0,4), function (data) {
            self.vue.recipes = data.recipes;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        })
    };


    self.get_more = function () {
        var num_recipes = self.vue.recipes.length;
        $.getJSON(get_recipes_url(num_recipes, num_recipes + 4), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.recipes, data.recipes);
        });
    };



    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            has_more: false,
            logged_in: true,
            recipes: [],
            name: null,
        },
        methods: {
            get_more: self.get_more,
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
