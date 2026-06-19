// =========================================================
// Plotly Resize Observer (GLOBAL - define once)
// =========================================================

// const resizeObserver = new ResizeObserver(entries => {
//     for (const entry of entries) {
//         const el = entry.target;
//         if (el.__plotly__) {
//             Plotly.Plots.resize(el);
//         }
//     }
// });


document.querySelectorAll(".download-btn").forEach(btn => {

    btn.addEventListener("click",  async event => {

        const filename = event.currentTarget.dataset.file;

        console.log(filename);

        
        // Fetch file
        const response = await fetch(`/download/${filename}`);
    
        if (!response.ok) {
            console.error("Download failed");
            return;
        }

        const blob = await response.blob();

        // Create temporary URL
        const url = URL.createObjectURL(blob);
    
        // Create hidden download link
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;

        // Trigger download
        a.click();

        // Cleanup
        URL.revokeObjectURL(url);
    
    
    
    });

});






function initExamplePlots() {
    const cards = document.querySelectorAll(".plot-card");

    for (const card of cards) {

        const container = card.querySelector(".plotly-container");
        const script = card.querySelector(".plot-data");

        if (!container || !script) continue;

        if (container.__rendered) continue;

        let figure;
        try {
            figure = JSON.parse(script.textContent);
        } catch (e) {
            console.error("Invalid plot JSON", e);
            continue;
        }

        Plotly.newPlot(container, figure.data, figure.layout, {
            responsive: true,
            displayModeBar: true
        });

        container.__rendered = true;
    }
}


// document.addEventListener("DOMContentLoaded", () => {
//     // only initialize if page is already visible
//     const examplesPage = document.getElementById("examples-page");

//     if (examplesPage.classList.contains("active-page")) {
//         initExamplePlots();
//     }
// });