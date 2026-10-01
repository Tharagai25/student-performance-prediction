document.getElementById("predictionForm").addEventListener("submit", async function (event) {

    event.preventDefault();

    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Predicting...";

    // Get form values
    const data = {

        // Categorical values
        school: document.getElementById("school").value,
        sex: document.getElementById("sex").value,
        address: document.getElementById("address").value,
        famsize: document.getElementById("famsize").value,
        Pstatus: document.getElementById("Pstatus").value,

        // Numerical values
        age: Number(document.getElementById("age").value),
        Medu: Number(document.getElementById("Medu").value),
        Fedu: Number(document.getElementById("Fedu").value),

        // Categorical values
        Mjob: document.getElementById("Mjob").value,
        Fjob: document.getElementById("Fjob").value,
        reason: document.getElementById("reason").value,
        guardian: document.getElementById("guardian").value,

        // Numerical values
        traveltime: Number(document.getElementById("traveltime").value),
        studytime: Number(document.getElementById("studytime").value),
        failures: Number(document.getElementById("failures").value),

        // Yes / No values
        schoolsup: document.getElementById("schoolsup").value,
        famsup: document.getElementById("famsup").value,
        paid: document.getElementById("paid").value,
        activities: document.getElementById("activities").value,
        nursery: document.getElementById("nursery").value,
        higher: document.getElementById("higher").value,
        internet: document.getElementById("internet").value,
        romantic: document.getElementById("romantic").value,

        // Numerical values
        famrel: Number(document.getElementById("famrel").value),
        freetime: Number(document.getElementById("freetime").value),
        goout: Number(document.getElementById("goout").value),
        Dalc: Number(document.getElementById("Dalc").value),
        Walc: Number(document.getElementById("Walc").value),
        health: Number(document.getElementById("health").value),
        absences: Number(document.getElementById("absences").value)
    };


    try {

        // Send data to deployed Render backend
        const response = await fetch(
            "https://student-performance-backend-qkik.onrender.com/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        const result = await response.json();


        if (response.ok) {

            resultDiv.innerHTML =
                "Predicted Final Grade (G3): " +
                result.predicted_score;

        } else {

            resultDiv.innerHTML =
                "Error: " +
                (result.error || "Prediction failed");

        }

    } catch (error) {

        console.error("Error:", error);

        resultDiv.innerHTML =
            "Unable to connect to the prediction server.";

    }

});