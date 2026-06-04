




const barcodeBtn = document.getElementById("barcodeBtn");

barcodeBtn.addEventListener("click", async () => {

    const file = window.__uploadedFile;

    if (!file) {
        alert("Please upload a file first");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

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
});