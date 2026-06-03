// =========================================================
// FILE INPUT EVENTS
// Handles drag/drop and file selection
// =========================================================
dropZone.onclick = () => fileInput.click();

fileInput.onchange = e => handleFile(e.target.files[0]);

dropZone.addEventListener("dragover", () =>
  dropZone.classList.add("dragover")
);

dropZone.addEventListener("dragleave", () =>
  dropZone.classList.remove("dragover")
);

dropZone.addEventListener("drop", e => {
  dropZone.classList.remove("dragover");
  handleFile(e.dataTransfer.files[0]);
});



// =========================================================
// FILE HANDLING PIPELINE
// Reads file → parses → sanitizes → analyzes → renders UI
// =========================================================
function handleFile(file) {

    // Store original file for backend upload
    window.__uploadedFile = file;
 
   // Reset preview rows
   previewInput.value = 10;
 
   spinner.classList.remove("hidden");
 
   const reader = new FileReader();
   // #######
   const formData = new FormData();
   formData.append("file", file);
 
   fetch("/upload", {
   method: "POST",
   body: formData
   })
   .then(async response => {
 
   const result = await response.json();
   console.log(result);
 
   if (!response.ok) {
     throw new Error(result.error || "Upload failed JS");
   }
 
   window.__lastData = result.data;
 
   updateUI(file, result);
 
   renderPreview(result.data);
 
  //  renderTable(result.data);
 
   diagramCards.forEach(card => {
     card.classList.remove("hidden");
   });

   barCodeCards.forEach(card => {
    card.classList.remove("hidden");
  });
 
   spinner.classList.add("hidden");
 
 })
 .catch(err => {
 
   errorMsg.textContent = err.message;
 
   spinner.classList.add("hidden");
 
 });
 }