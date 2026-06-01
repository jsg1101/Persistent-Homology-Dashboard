


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