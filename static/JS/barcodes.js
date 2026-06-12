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

    // Prime check
    if (!isPrime(prime)) {

        alert(
            `${prime} is not a prime number.\n\nPlease enter a prime coefficient.`
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