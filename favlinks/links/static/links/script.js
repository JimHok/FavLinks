document.addEventListener("DOMContentLoad", typeWriter, false);

var typeWriter = function (selector, type, interval) {
  var el = document.querySelectorAll(selector), // Getting elements in the DOM
    i = 0,
    len = el.length, // Length of element on the page
    list = [], // List of elements on the page in the DOM
    a,
    all,
    text,
    start,
    end,
    nextText,
    sectionId = selector.replace(/^#/, ""),
    targetSection = document.getElementById(sectionId),
    sections = document.getElementsByTagName("section")[0],
    targetSiblings = [].slice
      .call(sections.parentNode.children)
      .filter(function (v) {
        return v !== targetSection;
      }),
    cmd = document.querySelector(".command"),
    clear;

  for (; i < len; i++) {
    list.push(el[i]); // Pushing the element in the list array
  }

  for (a in list) {
    all = list[a]; // List of all element
    text = all.innerHTML; // InnerHTML of the elements
    start = 0; // Start index of the text in the elements
    end = 0; // End index of the text in the elements

    //Setting the default interval to 100 when interval is not set by the user
    if (typeof interval === "undefined") {
      interval = 100;
    }

    if (arguments[1] === "true") {
      setTimeout(function () {
        targetSection.classList.add("open");
      }, 200);

      for (var i = 0; i < targetSiblings.length; i++) {
        targetSiblings[i].classList.remove("open");
      }

      clear = setInterval(function () {
        // Animation start
        var newText = text.substr(start, end);

        all.innerHTML = newText;

        end = end + 1; //loops through the text in the element

        if (newText === text) {
          clearInterval(clear); // Animation end
          cmd.classList.add("open");
          input.focus();
        }
      }, interval);
    }

    return all;
  }
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    let cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var input = document.querySelector("input"),
  block = document.getElementsByTagName("section"),
  commandHistory = [];

window.onload = function () {
  typeWriter("#home", "true", 1);
  var sectionArray = [];
  for (var i = 0; i < block.length; i++) {
    sectionArray.push(block[i].id);
  }

  input.addEventListener("keyup", function (e) {
    if ((e.keyCode || e.which) == 13) {
      var inputValue = input.value.split(" ");
      commandHistory.push(inputValue);
      var targetValue = inputValue[0];
      var destination = "#" + targetValue;

      if (targetValue == "add") {
        var url = inputValue[1];
        var formData = new FormData();
        formData.append("method", "add");
        formData.append("url", url);
        if (inputValue.length == 3) {
          var category = inputValue[2];
          formData.append("category", category);
        }

        fetch("", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: formData,
        })
          .then((response) => response.text())
          .then((result) => console.log(result))
          .catch((error) => console.error("Error:", error));
      }

      if (targetValue == "update") {
        var id = inputValue[1];
        var url = inputValue[2];
        var formData = new FormData();
        formData.append("method", "update");
        formData.append("id", id);
        formData.append("url", url);
        if (inputValue.length == 4) {
          var category = inputValue[3];
          formData.append("category", category);
        }

        fetch("", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: formData,
        })
          .then((response) => response.text())
          .then((result) => console.log(result))
          .catch((error) => console.error("Error:", error));
      }

      if (targetValue == "delete") {
        var id = inputValue[1];
        var formData = new FormData();
        formData.append("method", "delete");
        formData.append("id", id);

        fetch("", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: formData,
        })
          .then((response) => response.text())
          .then((result) => console.log(result))
          .catch((error) => console.error("Error:", error));
      }

      typeWriter(destination, "true", 1);
      input.value = "";

      if (sectionArray.includes(targetValue) == false) {
        typeWriter("#error", "true", 1);
      }
    }
  });
};
