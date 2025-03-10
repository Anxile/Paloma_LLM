document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("userprofile")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // 防止默认表单提交行为

      // 创建一个 FormData 对象，读取表单数据
      const formData = new FormData(this);

      // 将 FormData 转换为一个普通的对象
      const data = {};
      const availableDays = []; // 用于存储申请人有空的天数
      data.sexualOrientation = formData.get("sexualOrientation");
      formData.forEach((value, key) => {
        // 如果字段是复选框，并且选中，将其设置为 true
        if (
          key === "Monday" ||
          key === "Tuesday" ||
          key === "Wednesday" ||
          key === "Thursday" ||
          key === "Friday" ||
          key === "Saturday" ||
          key === "Sunday"
        ) {
          availableDays.push(key); // 将有空的天数添加到数组中
        } else {
          data[key] = value;
        }
      });

      data.availableDays = availableDays; // 将有空的天数数组添加到数据对象中

      console.log("Form data:", data); // 调试输出

      // 获取 CSRF 令牌
      const csrfToken = formData.get("csrfmiddlewaretoken");

      // 使用 fetch 发送 POST 请求，内容类型为 application/json
      fetch("/api/submit/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken, // 添加 CSRF 令牌到请求头
        },
        body: JSON.stringify(data), // 转换为 JSON 字符串
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((result) => {
          console.log("Success:", result); // 调试输出
        })
        .catch((error) => {
          console.error("Error:", error); // 调试输出
        });
    });
});
