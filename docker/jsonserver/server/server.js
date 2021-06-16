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

server.post("/auth", (req, resp) => {
  console.log(req.body['username'])
  if(req.body && req.body['username'] === 'invaliduser'){
    resp.status(400).json({ "non_field_errors": ["Unable to log in with provided credentials."]});
  } else {
    resp.status(200).json({ token: "dummytoken"});
  }
});
server.get("/upload", (req, resp) => {
  resp.status(200).json({ uploadFilesCount: "0" });
});
server.get("/uploaded_file_count", (req, resp) => {
  resp.status(200).json({ count: "1" });
});
server.post("/upload", (req, resp) => {
  if(Number(req.headers['content-length']) < 10000){
    resp.status(200).json({ result: "FAIL" });
  } else {
    resp.status(200).json({ result: "SUCCESS",  uploadFilesCount: "2"});
  }
});

server.use(router);
server.listen(33000, () => {
  console.log('JSON Server is running');
});
