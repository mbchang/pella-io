var express = require('express');
var path = require('path');

var app = express();

// app.set('views', path.join(__dirname, 'views'));
// app.set('view engine', 'ejs');

app.use(express.static(path.join(__dirname, 'public')));

// var index = require('./routes/index');
// app.use('/', index);

// app.listen(3000, function () {
//   console.log('Example app listening on port 3000!');
// });

module.exports = app;