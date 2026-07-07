// =========================================================
// Threshold Option
// =========================================================

// Enable/Disable threshold input

const useThresholdBarcode =
    document.getElementById("use-threshold-barcode");

const thresholdBarcode =
    document.getElementById("threshold_barcode");

useThresholdBarcode.addEventListener("change", () => {

    thresholdBarcode.disabled =
        !useThresholdBarcode.checked;

    if (!useThresholdBarcode.checked) {

        thresholdBarcode.value = "";

    }

});


// =========================================================
// Subsampling Option
// =========================================================

// Enable/Disable subsampling input

const useSubsampleBarcode =
    document.getElementById("use-subsample-barcode");

const subsampleBarcode =
    document.getElementById("subsample_barcode");

useSubsampleBarcode.addEventListener("change", () => {

    subsampleBarcode.disabled =
        !useSubsampleBarcode.checked;

    if (!useSubsampleBarcode.checked) {

        subsampleBarcode.value = "";

    }

});











const barcodeBtn = document.getElementById("barcodeBtn");

barcodeBtn.addEventListener("click", async () => {

    const file = window.__uploadedFile;

    if (!file) {
        alert("Please upload a file first");
        return;
    }

    // Hide previous barcode (if one exists)
    document
        .getElementById("barcode-container")
        .classList.add("hidden");

    // Gather form data
    const dimension =
        document.querySelector(
            'input[name="dimension_barcodes"]:checked'
        ).value;

    const metric =
        document.querySelector(
            'input[name="metric_barcodes"]:checked'
        ).value;

    const prime =
        document.getElementById("prime_barcodes").value;


    // Gather optional threshold
    const threshold =
        useThresholdBarcode.checked
        ? thresholdBarcode.value
        : "inf";

    // Gather optional subsampling
    const subsample =
        useSubsampleBarcode.checked
        ? subsampleBarcode.value
        : "";

    // Prime check
    if (!isPrime(prime)) {

        alert(
            `${prime} is not a prime number.\n\nPlease enter a prime p for Z/pZ..`
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
        document.getElementById("barcode-loading");

    loading.classList.remove("hidden");

    barcodeBtn.disabled = true;
    barcodeBtn.textContent = "Computing...";

    try {

        // Fetch
        const formData = new FormData();

        formData.append("file", file);
        formData.append("dimension", dimension);
        formData.append("metric", metric);
        formData.append("prime", prime);
        formData.append("threshold", threshold);
        formData.append("subsample", subsample);

        const response = await fetch("/barcodes", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Barcode generation failed");
        }

        const blob = await response.blob();

        // Plot
        const imageUrl = URL.createObjectURL(blob);

        document.getElementById("barcode-image").src = imageUrl;

        document
            .getElementById("barcode-container")
            .classList.remove("hidden");

    }
    catch (err) {

        console.error(err);

        alert(
            err.message ||
            "An unexpected error occurred while generating the barcode."
        );

    }
    finally {

        // Hide spinner and enable Btn
        loading.classList.add("hidden");

        barcodeBtn.disabled = false;
        barcodeBtn.textContent = "Compute Barcode";

    }

});