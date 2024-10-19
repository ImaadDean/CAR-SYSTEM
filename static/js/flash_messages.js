document.addEventListener("DOMContentLoaded", function () {
  var messages = JSON.parse(
    document.getElementById("flash-messages").textContent
  );
  messages.forEach(function (message) {
    alert(message);
  });
});
