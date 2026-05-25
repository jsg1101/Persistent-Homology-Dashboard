


// =========================================================
// UI UPDATE (summary panel)
// =========================================================
function updateUI(file, r) {
    fileSummary.classList.remove("hidden");
    filePreview.classList.remove("hidden");
  
    // fileName.textContent = "NAME: " + file.name;
    // fileSize.textContent = "SIZE: " + (file.size / 1024).toFixed(1) + " KB";
  
    fileName.textContent =  file.name;
    fileSize.textContent =   (file.size / 1024).toFixed(1) + " KB";
  
  
    // rowCount.textContent = r.flagged.length - 1;
    rowCount.textContent = r.rows;
    // colCount.textContent = r.flagged[0]?.length || 0;
    colCount.textContent = r.cols;
  
    missingEl.textContent = r.missing;
    invalidEl.textContent = r.invalid;
    totalEl.textContent = r.total_issues;
  }
  
  
  
  // =========================================================
  // FULL TABLE RENDERING (all rows)
  // =========================================================
  function renderTable(data) {
    table.innerHTML = "";
  
    data.forEach((row, i) => {
      const tr = document.createElement("tr");
  
      row.forEach(c => {
        const el = document.createElement(i === 0 ? "th" : "td");
        el.textContent = c.value;
  
        if (c.type === "missing") el.classList.add("cell-missing");
        if (c.type === "invalid") el.classList.add("cell-invalid");
  
        tr.appendChild(el);
      });
  
      table.appendChild(tr);
    });
  }