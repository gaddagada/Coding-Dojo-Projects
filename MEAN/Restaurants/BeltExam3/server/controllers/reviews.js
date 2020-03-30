var mongoose = require("mongoose");
var Review = mongoose.model("Review");


module.exports = {
    editRestaurantsReviewsById: function(req, res){
        const review = Review.findOne({_id: req.params.id}, (err, review) => {
            console.log("Reviews.js procesing review request")
            if (err) {
                console.log("Reviews.js restaurant not found")
                res.status(400).json(err);
            } else {
                console.log("Reviews.js saving review")
                review.name = req.body.name;
                review.content = req.body.content;
                review.star = req.body.star;
                review.save( (error) => {
                if (error) {
                    console.log("Reviews.js invalid review data")
                    res.status(400).json(error);
                } else {
                    console.log("Reviews.js saving review data")
                    res.json({message: 'Success', data: review});
                }
            })
            }
        })
    },
    deleteRestaurantsReviewsById: function(req, res){
        Review.remove({_id: req.params.id}, (err) => {
            if (err) {
                res.status(400).json(err);
            } else {
                res.json({message: 'Successfully deleted'});
            }
        }
    )
    }
}