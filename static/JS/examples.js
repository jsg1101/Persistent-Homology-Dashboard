


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






document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".plot-card");

    for (const card of cards) {

        const container = card.querySelector(".plotly-container");
        const script = card.querySelector(".plot-data");

        if (!container || !script) continue;

        let figure;

        try {
            figure = JSON.parse(script.textContent);
        } catch (e) {
            console.error("Invalid plot JSON", e);
            continue;
        }

        delete figure.layout?.width;
        delete figure.layout?.height;

        figure.layout = {
            ...figure.layout,
            autosize: true,
            margin: { l: 0, r: 0, t: 0, b: 0 }
        };

        Plotly.newPlot(
            container,
            figure.data,
            figure.layout,
            {
                responsive: true,
                displayModeBar: true
            }
        );
    }
});