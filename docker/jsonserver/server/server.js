const jsonServer = require('json-server');
const fs = require("fs");
const server = jsonServer.create();
const data = require('./data/data.json');
const router = jsonServer.router('./data/data.json');
const middlewares = jsonServer.defaults();
const cors = require('cors');

const db = JSON.parse(fs.readFileSync("./data/data.json", "UTF-8"));

server.use(
    cors({
        origin: true,
        credentials: true,
        preflightContinue: false,
        methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    })
);
server.options('*', cors());

server.use(middlewares);
server.use(jsonServer.bodyParser);

server.use(router);
server.listen(33000, () => {
    console.log('JSON Server is running');
});
