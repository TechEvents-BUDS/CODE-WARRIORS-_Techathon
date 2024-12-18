document.getElementById("predictButton").addEventListener("click", function() {
    this.textContent = "Fetching Predictions...";
    this.disabled = true;
    document.getElementById("result").classList.add("hidden");

    fetch("/predict", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            const predictionList = document.getElementById("predictionList");
            predictionList.innerHTML = "";

            data.predictions.forEach((prediction, index) => {
                const listItem = document.createElement("li");
                listItem.textContent = `Day ${index + 1}: ${prediction.toFixed(2)} °C`;
                predictionList.appendChild(listItem);
            });

            document.getElementById("memoryUsageImage").src = "/static/memory_usage.png";
            document.getElementById("result").classList.remove("hidden");
            document.getElementById("predictButton").textContent = "Get Predictions";
            document.getElementById("predictButton").disabled = false;
        })
        .catch(error => {
            alert("Error fetching predictions.");
            this.textContent = "Get Predictions";
            this.disabled = false;
        });
});
