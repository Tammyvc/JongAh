/***************************************************
 * 数据来源白名单 *
 ***************************************************/

const accepted_origins = ["http://localhost", "http://192.168.1.1", "http://example.com"];

/*********************************************
 * 设置图片保存的文件夹 *
 *********************************************/
const imageFolder = "/Users/tammy/Desktop/my_file/JongAh/media/image/posts";

const fileInput = document.getElementsByClassName("tox-dropzone"); // assuming there is a file input element in the HTML with an ID of "fileInput"

fileInput.addEventListener("change", function() {
  const file = fileInput.files[0];
  const x_hr = new XMLHttpRequest();
  const formData = new FormData();
  formData.append("file", file);

  if (!file) {
    // 通知编辑器上传失败
    console.log("Upload failed.");
    return;
  }

  const xhr = new XMLHttpRequest();
  xhr.open("POST", "upload.php");
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      console.log(response.location);
    }
  };

  // 验证来源是否在白名单内
  const origin = window.location.origin;
  if (accepted_origins.includes(origin)) {
    xhr.setRequestHeader("Access-Control-Allow-Origin", origin);
  } else {
    console.log("Origin denied.");
    return;
  }

  /*
    如果脚本需要接收cookie，在init中加入参数 images_upload_credentials : true
    并加入下面两个被注释掉的header内容
  */
  // xhr.setRequestHeader("Access-Control-Allow-Credentials", "true");
  // xhr.setRequestHeader("P3P", "CP=\"There is no P3P policy.\"");

  // 简单的过滤一下文件名是否合格
  if (/\.*([^\w\s\d\-_~,;:\[\]\(\).])|([\.]{2,})/.test(file.name)) {
    console.log("Invalid file name.");
    return;
  }

  // 验证扩展名
  if (!["gif", "jpg", "png"].includes(file.name.split(".").pop().toLowerCase())) {
    console.log("Invalid extension.");
    return;
  }

  // 都没问题，就将上传数据移动到目标文件夹，此处直接使用原文件名，建议重命名
  xhr.send(formData);
});

