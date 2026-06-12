
function isPrime(n) {

    n = Number(n);

    if (n < 2) return false;

    for (let i = 2; i <= Math.sqrt(n); i++) {
        if (n % i === 0) {
            return false;
        }
    }

    return true;
}



const diagramBtn = document.getElementById("diagramBtn");

diagramBtn.addEventListener("click", async () => {

    const file = window.__uploadedFile;

    if (!file) {
        alert("Please upload a file first");
        return;
    }

    // Hide previous diagram (if one exists)
    document
        .getElementById("diagram-container")
        .classList.add("hidden");

    // Gather form data
    const dimension =
        document.querySelector(
            'input[name="dimension_diagram"]:checked'
        ).value;

    const metric =
        document.querySelector(
            'input[name="metric_diagram"]:checked'
        ).value;

    const prime =
        document.getElementById("prime_diagram").value;

    // Prime check
    if (!isPrime(prime)) {

        alert(
            `${prime} is not a prime number.\n\nPlease enter a prime coefficient.`
        );

        return;
    }

    // Show spinner and disable Btn
    const loading =
        document.getElementById("diagram-loading");

    loading.classList.remove("hidden");

    diagramBtn.disabled = true;
    diagramBtn.textContent = "Computing...";

    try {

        // Fetch
        const formData = new FormData();

        formData.append("file", file);
        formData.append("dimension", dimension);
        formData.append("metric", metric);
        formData.append("prime", prime);

        const response = await fetch("/diagrams", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Diagram generation failed");
        }

        const blob = await response.blob();

        // Plot
        const imageUrl = URL.createObjectURL(blob);

        document.getElementById("diagram-image").src = imageUrl;

        document
            .getElementById("diagram-container")
            .classList.remove("hidden");

    }
    catch (err) {

        console.error(err);

        alert(
            err.message ||
            "An unexpected error occurred while generating the diagram."
        );

    }
    finally {

        // Hide spinner and enable Btn
        loading.classList.add("hidden");

        diagramBtn.disabled = false;
        diagramBtn.textContent = "Compute Diagram";

    }

});