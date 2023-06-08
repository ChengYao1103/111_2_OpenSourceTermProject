import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js";
import {
  getDatabase,
  ref,
  get,
  query,
  limitToLast,
} from "https://www.gstatic.com/firebasejs/9.22.1/firebase-database.js";

// 設定 fireBase
import * as configs from "./configs.json" assert { type: "json" };
const firebaseConfig = configs.default.firebaseConfig;
const realtimeDatabaseNodeName = configs.default.realtimeDatabaseNodeName;

// 初始化 Firebase & Firestore
initializeApp(firebaseConfig);
const db = getDatabase();

// 半圓的周長
const length = 125;

var light = 50;
var temperature = 25;
var humidity = 50;
var lastWateredTime = "未有澆水紀錄";

// 從 fireBase 取得資料
async function getDataFromFirebase() {
  // 新資料固定會在最後一筆
  var q = query(ref(db, realtimeDatabaseNodeName), limitToLast(1));
  var response = await get(q);
  response.forEach((datas) => {
    // 如果有撈到資料就更新
    if (datas.exists()) {
      var data = datas.val();
      humidity = data.humidity;
      temperature = data.temperature;
      light = Math.round(data.lightness);
      // 如果從8266開機以來從未澆過水
      if (data.lastWateredTime === "2000-01-01 00:00:00") {
        lastWateredTime = "未有澆水紀錄";
      } else {
        lastWateredTime = data.lastWateredTime;
      }
    }
    // 沒撈到資料就設為 0
    else {
      humidity = 0;
      temperature = 0;
      light = 0;
      lastWateredTime = "未有澆水紀錄";
    }
  });
}

// 更新所有 progress bar
function updateProgressBars() {
  updateData("light", light);
  updateData("temperature", temperature);
  updateData("humidity", humidity);
  updateData("soil", lastWateredTime);
}

// 更新半圓 progress bar 的顯示狀態
function updateData(type, value) {
  // 取得顯示的 label
  var targetValue = document.getElementById(`${type}-value`);
  if (type === "temperature") {
    targetValue.innerHTML = `${value}°C`;
  } else if (type === "soil") {
    targetValue.innerHTML = `${value}`;
    return;
  } else {
    targetValue.innerHTML = `${value}%`;
  }
  // 取得目標動畫
  var targetAnimation = document.getElementById(`${type}-animation`);
  // 取得目前刻度，使動畫連貫
  var currentPosition = parseInt(
    targetAnimation.getAttribute("values").split("; ")[1]
  );
  // 如果是溫度的話刻度就只有50
  var part = type === "temperature" ? 50 : 100;
  // 更新目標值
  targetAnimation.setAttribute(
    "values",
    `${length - currentPosition}; ${length - (length / part) * value}`
  );
  // 重新跑過一遍動畫
  targetAnimation.beginElement();
}

// 每 10 分鐘更新一次資料
setInterval(async function () {
  await getDataFromFirebase();
  updateProgressBars();
}, 10 * 1000 * 60);

updateProgressBars();
await getDataFromFirebase();
updateProgressBars();
