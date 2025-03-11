document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("userprofile")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      const formData = new FormData(this);

      const data = {};
      const availableDays = [];
      const flavors = [];
      const economicConcept = [];
      const personality = [];
      data.sexualOrientation = formData.get("sexualOrientation");
      formData.forEach((value, key) => {
        if (
          key === "Monday" ||
          key === "Tuesday" ||
          key === "Wednesday" ||
          key === "Thursday" ||
          key === "Friday" ||
          key === "Saturday" ||
          key === "Sunday"
        ) {
          availableDays.push(key);
        } else {
          data[key] = value;
        }
      });

      formData.forEach((value, key) => {
        if (
          key === "Japanese Cuisine" ||
          key === "Indian Cuisine" ||
          key === "Canadian Cuisine" ||
          key === "Italian Cuisine" ||
          key === "Chinese Cuisine" ||
          key === "Mexican Cuisine" ||
          key === "American Cuisine"
        ) {
          flavors.push(key);
        }
      });

      formData.forEach((value, key) => {
        if (
          key === "Savings" ||
          key === "Consumption" ||
          key === "Investment" ||
          key === "Luxury enthusiasts" ||
          key === "Pragmatists" ||
          key === "Sharing economy" ||
          key === "Independent economy"
        ) {
          economicConcept.push(key);
        }
      });

      formData.forEach((value, key) => {
        if (
          key === "Extroverted" ||
          key === "Introverted" ||
          key === "Traditional" ||
          key === "Modern" ||
          key === "Adventurous" ||
          key === "Conservative" ||
          key === "Individualism" ||
          key === "Collectivism"
        ) {
          personality.push(key);
        }
      });

      data.availableDays = availableDays;
      data.cuisine = flavors;
      data.concept = economicConcept;
      data.p_and_v = personality;

      console.log("Form data:", data);

      const csrfToken = formData.get("csrfmiddlewaretoken");

      fetch("/api/submit/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            return response.text().then((text) => {
              throw new Error(text);
            });
          }
          return response.json();
        })
        .then((result) => {
          console.log("Success:", result);
          window.location.href =
            "/api/match_result/?result=" +
            encodeURIComponent(result.analysis_result);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
});

function updateOthersValue() {
  const othersRadio = document.getElementById("Others");
  const otherDegreeImput = document.getElementById("Otherdegree");
  if (othersRadio.checked) {
    othersRadio.value = otherDegreeImput.value;
  }
}
