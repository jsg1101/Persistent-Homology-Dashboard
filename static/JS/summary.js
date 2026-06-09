


// =========================================================
// UI UPDATE (summary panel and preview panel)
// =========================================================
function renderSummary(file, result) {


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
      rowCount.textContent = result.rows;
    });

     // Update all column counts
    colCounts.forEach(function(colCount) {
      colCount.textContent = result.cols;
    });

    // Update all missing elements
    missingEls.forEach(function(missingEl) {
      missingEl.textContent = result.missing;
    });

    // Update all invalid elements
    invalidEls.forEach(function(invalidEl) {
      invalidEl.textContent = result.invalid;
    });

    // Update all total issues elements
    totalEls.forEach(function(totalEl) {
      totalEl.textContent = result.total_issues;
    });




    fileSummaries.forEach(card => {

      const totalBox = card.querySelector(".issue-box.total");
      const statusIcon = card.querySelector(".issue-status-icon");
  
      totalBox.classList.remove("success", "error");
  
      if (result.total_issues === 0) {
  
          totalBox.classList.add("success");
          statusIcon.textContent = "✅";
  
      } else {
  
          totalBox.classList.add("error");
          statusIcon.textContent = "❌";
  
      }
  
    });

  }
  