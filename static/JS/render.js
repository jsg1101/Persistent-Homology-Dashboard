


// =========================================================
// UI UPDATE (summary panel)
// =========================================================
function updateUI(file, r) {


    // 1. Reveal all file summary cards
    fileSummaries.forEach(function(fileSummary) {
      fileSummary.classList.remove("hidden");
    });

    // Reveal the preview panel
    filePreview.classList.remove("hidden");
  
    // Update all file names
    fileNames.forEach(function(fileName) {
      fileName.textContent = file.name;
    });

    // Update all file sizes
    fileSizes.forEach(function(fileSize) {
      fileSize.textContent = (file.size / 1024).toFixed(1) + " KB";
    });
  
    // Update all row counts
    rowCounts.forEach(function(rowCount) {
      rowCount.textContent = r.rows;
    });

     // Update all column counts
    colCounts.forEach(function(colCount) {
      colCount.textContent = r.cols;
    });

    // Update all missing elements
    missingEls.forEach(function(missingEl) {
      missingEl.textContent = r.missing;
    });

    // Update all invalid elements
    invalidEls.forEach(function(invalidEl) {
      invalidEl.textContent = r.invalid;
    });

    // Update all total issues elements
    totalEls.forEach(function(totalEl) {
      totalEl.textContent = r.total_issues;
    });


  }
  
  
  
  // =========================================================
  // FULL TABLE RENDERING (all rows)
  // =========================================================
  // function renderTable(data) {
  //   table.innerHTML = "";
  
  //   data.forEach((row, i) => {
  //     const tr = document.createElement("tr");
  
  //     row.forEach(c => {
  //       const el = document.createElement(i === 0 ? "th" : "td");
  //       el.textContent = c.value;
  
  //       if (c.type === "missing") el.classList.add("cell-missing");
  //       if (c.type === "invalid") el.classList.add("cell-invalid");
  
  //       tr.appendChild(el);
  //     });
  
  //     table.appendChild(tr);
  //   });
  // }