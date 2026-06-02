




const diagramBtn = document.getElementById("diagramBtn");

diagramBtn.addEventListener("click", async () => {

    const file = window.__uploadedFile;

    if (!file) {
        alert("Please upload a file first");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/diagrams", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        console.error("Diagram generation failed");
        return;
    }

    const blob = await response.blob();

    const imageUrl = URL.createObjectURL(blob);

    document.getElementById("diagram-image").src = imageUrl;
});