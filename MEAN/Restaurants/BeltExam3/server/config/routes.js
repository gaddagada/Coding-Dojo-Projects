//The controller file 
var restaurants = require("../controllers/restaurants.js");
var reviews = require("../controllers/reviews.js");
var path = require("path");

module.exports = function(app){
    app.get("/restaurants", restaurants.index)

    app.get("/restaurants/:id", restaurants.detailsByRestaurantId)

    app.post("/restaurants/:id", restaurants.postRestaurantsById)

    app.post("/restaurants", restaurants.addRestaurants)

    app.put("/restaurants/:id", restaurants.editRestaurantsById)

    app.put("/reviews/:id", reviews.editRestaurantsReviewsById)

    app.delete("/restaurants/:id", restaurants.deleteRestaurantsById)

    app.delete("/reviews/:id", reviews.deleteRestaurantsReviewsById)

    app.all("*", (req,res,next) => {
        res.sendFile(path.resolve("./public/dist/public/index.html"))
    });
}