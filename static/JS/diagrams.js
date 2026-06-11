
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

    document
        .getElementById("diagram-container")
        .classList.remove("hidden");


});