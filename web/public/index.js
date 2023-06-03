import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js";
import {
  getDatabase,
  ref,
  get,
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
var lastWateredTime = "";

// 從 fireBase 取得資料
async function getDataFromFirebase() {
  var response = await get(ref(db, realtimeDatabaseNodeName));
  response.forEach((datas) => {
    // 如果有撈到資料就更新
    if (datas.exists()) {
      var data = datas.val();
      humidity = data.humidity;
      temperature = data.temperature;
      light = data.lightness;
      lastWateredTime = data.lastWateredTime;
    }
    // 沒撈到資料就設為 0
    else {
      humidity = 0;
      temperature = 0;
      light = 0;
      lastWateredTime = 0;
    }
  });
}

// 更新所有 progress bar
function updateProgressBar() {
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
    `${length - currentPosition}; ${125 - (length / part) * value}`
  );
  // 重新跑過一遍動畫
  targetAnimation.beginElement();
}

// 每 10 分鐘更新一次資料
setInterval(async function () {
  await getDataFromFirebase();
  updateProgressBar();
}, 10 * 1000 * 60);

updateProgressBar();
await getDataFromFirebase();
updateProgressBar();
