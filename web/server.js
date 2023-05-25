var express = require("express"),
  app = express();

// 設定路由根目錄
app.use(express.static("public"));

// 監聽 3000 port
port = 3000;
const server = app.listen(port, function () {
  console.log("Listening on " + port);
});

