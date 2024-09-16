var express = require('express');
var router = express.Router();

const users = [
	{
		id: 1,
		firstName: 'John',
		lastName: 'Smith',
		email: 'jsmith@gmail.com'
	},
	{
		id: 2,
		firstName: 'Sara',
		lastName: 'Connor',
		email: 'connors3899@gmail.com'
	},
	{
		id: 3,
		firstName: 'Jim',
		lastName: 'Dean',
		email: 'breakfastmeat@gmail.com'
	},
	{
		id: 4,
		firstName: 'Angelina',
		lastName: 'Jolie',
		email: 'lotsakids@gmail.com'
	}
]

/* GET users listing. */
router.get('/', function(req, res, next) {
	res.header('Access-Control-Allow-Origin', 'http://localhost:5173');

  res.json(users);
});

module.exports = router;
