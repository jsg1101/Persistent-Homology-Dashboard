const barcodeBtn = document.getElementById("barcodeBtn");

barcodeBtn.addEventListener("click", async () => {

    const file = window.__uploadedFile;

    if (!file) {
        alert("Please upload a file first");
        return;
    }

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

    if (!isPrime(prime)) {

        alert(
            `${prime} is not a prime number.\n\nPlease enter a prime coefficient.`
        );

        return;
    }

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
        console.error("Barcode generation failed");
        return;
    }

    const blob = await response.blob();

    const imageUrl = URL.createObjectURL(blob);

    document.getElementById("barcode-image").src = imageUrl;

    document
        .getElementById("barcode-container")
        .classList.remove("hidden");

});