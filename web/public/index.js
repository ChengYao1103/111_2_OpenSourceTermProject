import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js";
import {
  query,
  orderBy,
  limit,
  getFirestore,
  getDocs,
  collection,
} from "https://www.gstatic.com/firebasejs/9.22.1/firebase-firestore.js";
// 設定 fireBase
import * as configs from "./configs.json" assert { type: "json" };
const firebaseConfig = configs.default.firebaseConfig;

// 初始化 Firebase &  Firestore
initializeApp(firebaseConfig);
const db = getFirestore();

// 半圓的周長
const length = 125;

var light = 50;
var temperature = 25;
var humidity = 50;
var isSoilWet = 0;

// 從 fireBase 取得資料
async function getDataFromFirebase() {
  // 以最新的資料為主，只搜尋第1筆
  var q = query(collection(db, "sensor"), orderBy("time", "desc"), limit(1));
  var response = await getDocs(q);
  response.forEach((doc) => {
    // 如果有撈到資料就更新
    if (doc.data()) {
      var datas = doc.data();
      console.log(datas);
      humidity = datas.humidity;
      temperature = datas.temperature;
      light = datas.lightness;
      isSoilWet = datas.isSoilWet;
    }
    // 沒撈到資料就設為 0
    else {
      humidity = 0;
      temperature = 0;
      light = 0;
      isSoilWet = 0;
    }
  });
}

// 更新所有 progress bar
function updateProgressBar() {
  updateData("light", light);
  updateData("temperature", temperature);
  updateData("humidity", humidity);
}

// 更新半圓 progress bar 的顯示狀態
function updateData(type, value) {
  // 取得目標動畫
  var targetAnimation = document.getElementById(`${type}-animation`);
  // 如果是溫度的話刻度就只有50
  var part = type === "temperature" ? 50 : 100;
  // 更新目標值
  targetAnimation.setAttribute(
    "values",
    `${length}; ${125 - (length / part) * value}`
  );
  // 重新跑過一遍動畫
  targetAnimation.beginElement();
  // 取得顯示的 label
  var targetValue = document.getElementById(`${type}-value`);
  if (type === "temperature") {
    targetValue.innerHTML = `${value}°C`;
  } else {
    targetValue.innerHTML = `${value}%`;
  }
}

// 每 10 分鐘更新一次資料
setInterval(async function () {
  await getDataFromFirebase();
  updateProgressBar();
}, 10 * 1000 * 60);

updateProgressBar();
await getDataFromFirebase();
updateProgressBar();
