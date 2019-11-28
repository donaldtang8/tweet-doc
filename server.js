// import express JS module into app
// and creates its variable.
var express = require("express");
var bodyParser = require("body-parser");
var app = express();

app.set("view engine", "ejs");

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

let pyresults = null;
let results = null;

app.get("/", (req, res) => {
  res.render("home");
});

app.get("/about", (req, res) => {
  res.render("about");
});

app.get("/contact", (req, res) => {
  res.render("contact");
});

app.get("/sentiment", (req, res) => {
  if (results === null) {
    res.redirect("/");
  } else {
    res.render("results", { pos: results.pos, neg: results.neg, neut: results.neut, posCount: results.posCount, negCount: results.negCount, neutCount: results.neutCount });
  }
});

app.post("/sentiment", getSentiment);

function getSentiment(req, res) {
  var spawn = require("child_process").spawn;
  var process = spawn("python", ["./webscrape.py", req.body.username]);

  process.stdout.on("data", data => {
    pyresults = data.toString();
    results = JSON.parse(pyresults);
    res.render("results", { pos: results.pos, neg: results.neg, neut: results.neut, posCount: results.posCount, negCount: results.negCount, neutCount: results.neutCount });
  });
  // res.send(results);
}

let port = process.env.PORT;
if (port == null || port == "") {
  port = 3000;
}

app.listen(port, (req, res) => {
  console.log("server running on port 3000");
});
