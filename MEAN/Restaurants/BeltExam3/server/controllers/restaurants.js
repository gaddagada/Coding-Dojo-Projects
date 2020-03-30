var mongoose = require("mongoose");
var Restaurant = mongoose.model("Restaurant");
var Review = mongoose.model("Review");


module.exports = {

    index: function (req, res) {
        Restaurant.find({}, function (err, restaurants) {
            if (err) {
                res.status(400).json(err);
            } else {
                res.json({ message: 'Success', data: restaurants });
            }
        })
    },

    detailsByRestaurantId: function (req, res) {
        Restaurant.findOne({ _id: req.params.id })
            .populate({ path: 'reviews', options: { sort: { "star": "descending" } } })
            .exec((err, restaurant) => {
                if (err) {
                    res.status(400).json(err);
                } else {
                    res.json({ message: 'Success', data: restaurant });
                }
            })
    },

    postRestaurantsById: function (req, res) {
        console.log("postRestaurantsById")
        Restaurant.findOne({ _id: req.params.id }, (err, restaurant) => {
            const review = new Review(req.body);
            review._restaurant = restaurant._id;
            restaurant.reviews.push(review);
            //Save the review first.
            review.save((error) => {
                console.log("Review saved", req.params.id)
                if (error) {
                    console.log("Review save err", req.params.id)
                    res.json(error);
                } else {
                    console.log("Review save success", req.params.id)
                    //Set review on the restaurant
                    restaurant.save((err) => {
                        if (err) {
                            console.log("Restaurant Save error", req.params.id)
                            res.status(400).json(err);
                        } else {
                            console.log("Restaurant Save success", req.params.id)                
                            res.json({ message: 'Success', data: review });
                        }
                    })
                }
            })
        })
    },






    addRestaurants: function (req, res) {
        const restaurant = new Restaurant(req.body);
        console.log("Adding new restaurant", restaurant)
        Restaurant.findOne({ name: req.body.name }, (error, response) => {
            if (response) {
                res.json({ error: 'Restaurant with that name already exists' });
            } else {
                restaurant.save((err) => {
                    if (err) {
                        res.json(err);
                    } else {
                        res.json({ message: 'Success', data: restaurant });
                    }
                })
            }
        })
    },

    editRestaurantsById: function (req, res) {
        console.log("Eidting Restaurant :", req.params.id)
        console.log("Name :", req.body.name)
        console.log("Cuisine :", req.body.cuisine)
        console.log("Cuisine :", req.body.review)

        const restaurant = Restaurant.findOne({ _id: req.params.id }, (err, restaurant) => {
            if (err) {
                console.log("Eidting Restaurant Err :", req.params.id)
                res.status(400).json(err);
            } else {
                restaurant.name = req.body.name;
                restaurant.cuisine = req.body.cuisine;
                // restaurant.review = req.body.review;
                console.log("Eidting Restaurant Saving :", req.params.id)
                restaurant.save((error) => {
                    if (error) {
                        console.log("Eidting Restaurant Saving err :", req.params.id)
                        res.json(error);
                    } else {
                        console.log("Eidting Restaurant Saving success:", req.params.id)
                        res.json({ message: 'Success', data: restaurant });
                    }
                })
            }
            //console.log("Eidting Restaurant All done :", req.params.id)
        })
    },





    deleteRestaurantsById: function (req, res) {
        Restaurant.remove({ _id: req.params.id }, (err) => {
            if (err) {
                res.status(400).json(err);
            } else {
                res.json({ message: 'Successfully deleted' });
            }
        })
    },
}