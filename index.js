require("dotenv").config();

const { Telegraf } = require("telegraf");
const LocalSession = require("telegraf-session-local");

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.use(new LocalSession().middleware());

const startMessage =
  "Hello, this bot will notify you if your tests are uploaded to jExam. \n Add courses with `/add <course>` . \n List all courses with `/stats` . \n You can delete all courses with `/remove` .";

bot.start((ctx) => ctx.replyWithMarkdown(startMessage));
bot.help((ctx) => ctx.replyWithMarkdown(startMessage));

bot.command("/add", (ctx) => {
  msg = ctx.message.text;
  course = msg.substr(msg.indexOf(" ") + 1);
  if (course.startsWith("/")) {
    ctx.replyWithMarkdown(
      "Wrong usage, you can add courses with `/add <course>` ."
    );
  } else {
    ctx.session.courses = ctx.session.courses || [];
    ctx.session.courses.push(course);
    ctx.replyWithMarkdown(`Observed courses: \`${ctx.session.courses}\``);
  }
});

bot.command("/stats", (ctx) => {
  ctx.replyWithMarkdown(
    `Saved courses \`${ctx.session.courses}\` from @${
      ctx.from.username || ctx.from.id
    }`
  );
});

bot.command("/remove", (ctx) => {
  ctx.replyWithMarkdown(
    `Removing session from database: \`${JSON.stringify(ctx.session)}\``
  );
  ctx.session = null;
});

bot.launch();

// Enable graceful stop
process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
