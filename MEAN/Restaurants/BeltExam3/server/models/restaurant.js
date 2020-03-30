var mongoose = require("mongoose");
let Schema = mongoose.Schema;

var RestaurantSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Please enter Restaurant Name'],
        minlength: [3, 'Restuarant Name has to be at least three characters long'],
        trim: true
    },
    cuisine: {
        type: String,
        required: [true, 'Please enter Restaurant Cuisine'],
        minlength: [3, 'Restuarant Cuisine has to be at least three characters long'],
        trim: true
    },
    reviews: [{
        type: Schema.Types.ObjectId,
        ref: 'Review'
    }]
    }, {timestamps: true})

    ReviewSchema = new mongoose.Schema({
        _restaurant: {
        type: Schema.Types.ObjectId,
        ref: 'Restaurant'
        },
        name: {
        type: String,
        required: [true, 'Please enter name'],
        minlength: [3, 'Name should be at least three characters long'],
        trim: true
        },
        star: {
        type: Number,
        default: 1,
        min: [1, 'Every Restaurant deserves at least one star'],
        max: [5, 'Unfortunately, we cannot give a restaurant more than five stars']
        },
        content: {
        type: String,
        required: [true, 'Please enter review'],
        minlength: [3, 'Review should be at least three characters long'],
        trim: true
        }
    }, {timestamps: true})

mongoose.model('Restaurant', RestaurantSchema);
mongoose.model('Review', ReviewSchema);