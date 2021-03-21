require("dotenv").config();
fs = require('fs');

const { Telegraf } = require("telegraf");
const LocalSession = require("telegraf-session-local"); 

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.use(new LocalSession().middleware());

const startMessage =
  "Hello, this bot will notify you if your tests are uploaded to jExam. \n Add courses with `/add <course>` . \n List all courses with `/stats` . \n You can delete all courses with `/remove` .";

bot.start((ctx) => ctx.replyWithMarkdown(startMessage));
bot.help((ctx) => ctx.replyWithMarkdown(startMessage));

bot.command("/add", (ctx) => {
  var j = JSON.parse(fs.readFileSync('sessions.json', 'utf8'));
  var userID = ctx.from.id;
  var exists = false;
  j.sessions.forEach(function(obj) {
    if (obj.id == userID) { exists = true; }
  });
  msg = ctx.message.text;
  course = msg.substr(msg.indexOf(" ") + 1);
  if (course.startsWith("/")) {
    ctx.replyWithMarkdown(
      "Wrong usage, you can add courses with `/add <course>` ."
    );
  } else {
    if (!exists) {
      var newSession = {"id" : userID.toString(), "courses" : [ course ]};
      j.sessions.push(newSession);
    } else {
      j.sessions.forEach(function(obj) {
        if (obj.id == userID) { obj.courses.push(course) }
      });
    }

    var courses = "none";
    j.sessions.forEach(function(obj) {
      if (obj.id == userID) {
        courses = Array.prototype.join.call(obj.courses);
      }
    });

    ctx.replyWithMarkdown(`Observed courses: \`${courses}\``);
    var output = JSON.stringify(j, null, 4);
    fs.writeFile('sessions.json', output, function (err) {
      if (err) return console.log(err);
    });
  }
});

bot.command("/stats", (ctx) => {
  var j = JSON.parse(fs.readFileSync('sessions.json', 'utf8'));
  var userID = ctx.from.id;
  var courses = "none";
  j.sessions.forEach(function(obj) {
    if (obj.id == userID) {
      courses = Array.prototype.join.call(obj.courses);
    }
  });

  ctx.replyWithMarkdown(
    `Saved courses: \`${courses}\` for user: @${
      ctx.from.username || ctx.from.id
    }`
  );
});

bot.command("/remove", (ctx) => {
  var j = JSON.parse(fs.readFileSync('sessions.json', 'utf8'));
  var userID = ctx.from.id;
  var courses = "";

  j.sessions.forEach(function(obj) {
    if (obj.id == userID) {
      courses = Array.prototype.join.call(obj.courses);
    }
  });

  ctx.replyWithMarkdown(
    `Removing session from database: \`${courses}\` for user: @${
      ctx.from.username || ctx.from.id
    }`
  );
  ctx.session = null;
});

bot.launch();

// Enable graceful stop
process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
