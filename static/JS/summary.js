


// =========================================================
// UI UPDATE (summary panel and preview panel)
// =========================================================
function renderSummary(file, r) {


    // Reveal all file summary cards
    fileSummaries.forEach(function(fileSummary) {
      fileSummary.classList.remove("hidden");
    });

    // Reveal the preview panel
    // filePreview.classList.remove("hidden");
  
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
  