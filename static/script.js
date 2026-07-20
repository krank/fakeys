const theForm = document.querySelector("form");
const logElement = document.querySelector(".log");

theForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  logElement.innerHTML = "Waiting for response…";

  let formData = new FormData(theForm);
  
  let response = await fetch("/type_string/", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(Object.fromEntries(formData.entries())),
  });

  result = await response.json();

  logElement.innerHTML = "";

  addLogItem(`${response.status}: ${result.message}`);
  
  if (result.errors) {
    result.errors.forEach(error => {
      addLogItem(`${error.loglevel}: ${error.message}`)
    });
  }
  
});

function addLogItem(content) {
  logItemElement = document.createElement("p");
  logItemElement.append(content);
  logElement.append(logItemElement);
}