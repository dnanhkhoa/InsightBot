const translate = require('google-translate-api');
const bodyparser = require('body-parser');
const express = require('express');

const app = express();
const port = process.env.PORT || 8080;

app.use(bodyparser.json()); // For supporting json encoded bodies
app.use(bodyparser.urlencoded({ extended: true })); // For supporting encoded bodies

app.get('/', (req, res) => {
    res.send('Insight Bot Service is running!');
});

app.post('/api/googletranslate', (req, res) => {
    var msg = req.body.msg;
    res.send(msg);
});

app.listen(port, (err) => {
    if (err) {
        console.log('Something bad happened!', err);
    }
    console.log(`Insight Bot Service is running on ${port}!`);
});
