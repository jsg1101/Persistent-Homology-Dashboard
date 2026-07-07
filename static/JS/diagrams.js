
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


// =========================================================
// Threshold Option
// =========================================================

// Enable/Disable threshold input

const useThresholdDiagram =
    document.getElementById("use-threshold-diagram");

const thresholdDiagram =
    document.getElementById("threshold_diagram");

useThresholdDiagram.addEventListener("change", () => {

    thresholdDiagram.disabled =
        !useThresholdDiagram.checked;

    if (!useThresholdDiagram.checked) {

        thresholdDiagram.value = "";

    }

});


// =========================================================
// Subsampling Option
// =========================================================

// Enable/Disable subsampling input

const useSubsampleDiagram =
    document.getElementById("use-subsample-diagram");

const subsampleDiagram =
    document.getElementById("subsample_diagram");

useSubsampleDiagram.addEventListener("change", () => {

    subsampleDiagram.disabled =
        !useSubsampleDiagram.checked;

    if (!useSubsampleDiagram.checked) {

        subsampleDiagram.value = "";

    }

});



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

    // Gather optional threshold
    const threshold =
        useThresholdDiagram.checked
        ? thresholdDiagram.value
        : "inf";

    // Gather optional subsampling
    const subsample =
        useSubsampleDiagram.checked
        ? subsampleDiagram.value
        : "";

    // Prime check
    if (!isPrime(prime)) {

        alert(
            `${prime} is not a prime number.\n\nPlease enter a prime p for Z/pZ.`
        );

        return;
    }

    // Optional Threshold check
    if (threshold <= 0) {

        alert(
            `The epsilon thershold must be a positive number.\n\nPlease enter a threshold greater than zero.`
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
        formData.append("threshold", threshold);
        formData.append("subsample", subsample);

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