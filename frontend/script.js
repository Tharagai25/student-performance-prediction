const form = document.getElementById("predictionForm");
const result = document.getElementById("predictionText");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    result.innerText = "Predicting...";

    const data = {

        school: document.getElementById("school").value,
        sex: document.getElementById("sex").value,
        age: Number(document.getElementById("age").value),
        address: document.getElementById("address").value,
        famsize: document.getElementById("famsize").value,
        Pstatus: document.getElementById("Pstatus").value,

        Medu: Number(document.getElementById("Medu").value),
        Fedu: Number(document.getElementById("Fedu").value),

        Mjob: document.getElementById("Mjob").value,
        Fjob: document.getElementById("Fjob").value,
        reason: document.getElementById("reason").value,
        guardian: document.getElementById("guardian").value,

        traveltime: Number(document.getElementById("traveltime").value),
        studytime: Number(document.getElementById("studytime").value),
        failures: Number(document.getElementById("failures").value),

        schoolsup: document.getElementById("schoolsup").checked ? "yes" : "no",
        famsup: document.getElementById("famsup").checked ? "yes" : "no",
        paid: document.getElementById("paid").checked ? "yes" : "no",
        activities: document.getElementById("activities").checked ? "yes" : "no",
        nursery: document.getElementById("nursery").checked ? "yes" : "no",
        higher: document.getElementById("higher").checked ? "yes" : "no",
        internet: document.getElementById("internet").checked ? "yes" : "no",
        romantic: document.getElementById("romantic").checked ? "yes" : "no",

        famrel: Number(document.getElementById("famrel").value),
        freetime: Number(document.getElementById("freetime").value),
        goout: Number(document.getElementById("goout").value),

        Dalc: Number(document.getElementById("Dalc").value),
        Walc: Number(document.getElementById("Walc").value),

        health: Number(document.getElementById("health").value),
        absences: Number(document.getElementById("absences").value)
    };

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        const resultData = await response.json();

        if (response.ok) {

            result.innerText =
                "Predicted Final Grade (G3): " +
                resultData.predicted_score;

        } else {

            result.innerText =
                "Error: " + resultData.error;
        }

    } catch (error) {

        result.innerText =
            "Unable to connect to backend. Please make sure Flask server is running.";

        console.error(error);
    }

});