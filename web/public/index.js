// 半圓的周長
const length = 125;

var light = 50;
var temperature = 25;
var humidity = 50;

// 更新半圓 progress bar 的顯示狀態
function updateProgressBar() {
  updateData("light", light);
  updateData("temperature", temperature);
  updateData("humidity", humidity);
}

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

setInterval(function () {
  updateProgressBar();
  light += 1;
  humidity -= 1;
  temperature += 1;
}, 2000);
