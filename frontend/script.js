const form = document.getElementById("churnForm");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const customerData = {
        gender: document.getElementById("gender").value,
        SeniorCitizen: Number(document.getElementById("SeniorCitizen").value),
        Partner: document.getElementById("Partner").value,
        Dependents: document.getElementById("Dependents").value,
        tenure: Number(document.getElementById("tenure").value),
        PhoneService: document.getElementById("PhoneService").value,
        MultipleLines: document.getElementById("MultipleLines").value,
        InternetService: document.getElementById("InternetService").value,
        OnlineSecurity: document.getElementById("OnlineSecurity").value,
        OnlineBackup: document.getElementById("OnlineBackup").value,
        DeviceProtection: document.getElementById("DeviceProtection").value,
        TechSupport: document.getElementById("TechSupport").value,
        StreamingTV: document.getElementById("StreamingTV").value,
        StreamingMovies: document.getElementById("StreamingMovies").value,
        Contract: document.getElementById("Contract").value,
        PaperlessBilling: document.getElementById("PaperlessBilling").value,
        PaymentMethod: document.getElementById("PaymentMethod").value,
        MonthlyCharges: Number(document.getElementById("MonthlyCharges").value),
        TotalCharges: Number(document.getElementById("TotalCharges").value)
    };

    try {

        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(customerData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Prediction failed.");
        }

        document.getElementById("result").classList.remove("hidden");

        document.getElementById("probability").textContent =
            result.churn_probability + "%";

        document.getElementById("prediction").textContent =
            result.prediction;

    } catch (error) {

        alert("Error: " + error.message);

    }

});