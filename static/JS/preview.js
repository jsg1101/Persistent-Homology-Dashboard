


// =========================================================
// PREVIEW RENDERING 
// =========================================================
  function renderPreview(data) {

    // Reveal the preview panel
    filePreview.classList.remove("hidden");

    previewTable.innerHTML = "";
  
    const count = Number(previewInput.value);
    const safeCount = Number.isNaN(count) ? 10 : count;
  
    data.slice(0, safeCount).forEach((row, i) => {

      const tr = document.createElement("tr");
  
      row.forEach(c => {

        const el = document.createElement("td");

        el.textContent = c.value;
        
        // label cells
        if (c.type === "missing") el.classList.add("cell-missing");
        if (c.type === "invalid") el.classList.add("cell-invalid");
  
        tr.appendChild(el);
      });
  
      previewTable.appendChild(tr);

    });
  
    updatePreviewHeight();
  }


// =========================================================
// PREVIEW CONTROLS
// Updates preview when row count changes
// =========================================================
previewInput.addEventListener("input", () => {
  if (window.__lastData) {
    renderPreview(window.__lastData);
    updatePreviewHeight();
    }
  });
  
  // =========================================================
  // PREVIEW TOGGLE (expand / collapse)
  // =========================================================
  let open = false;
  
  toggleBtn.onclick = () => {
    open = !open;
  
    if (open) {
      previewSection.classList.add("preview-expanded");
      previewSection.style.maxHeight = previewSection.scrollHeight + "px";
      toggleBtn.textContent = "Hide Preview ▲";
    } else {
      previewSection.classList.remove("preview-expanded");
      previewSection.style.maxHeight = "0px";
      toggleBtn.textContent = "Show Preview ▼";
    }
  };



// =========================================================
// PREVIEW HEIGHT MANAGEMENT (smooth animation)
// =========================================================
function updatePreviewHeight() {
    if (previewSection.classList.contains("preview-expanded")) {
      previewSection.style.maxHeight = previewSection.scrollHeight + "px";
    }
}
  
  