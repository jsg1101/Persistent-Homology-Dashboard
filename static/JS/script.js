// =========================================================
// GLOBAL DRAG PREVENTION
// Prevent browser from opening dropped files
// =========================================================
document.addEventListener("dragover", e => e.preventDefault());
document.addEventListener("drop", e => e.preventDefault());

// =========================================================
// INITIAL SETUP
// Reset preview input on page load (browser may persist value)
// =========================================================
window.addEventListener("DOMContentLoaded", () => {
  previewInput.value = 10;
});

// =========================================================
// DOM ELEMENT REFERENCES
// Centralized access to all UI elements
// =========================================================
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

const spinner = document.getElementById("spinner");
const errorMsg = document.getElementById("errorMsg");

const fileSummary = document.getElementById("fileSummary");

const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");

const rowCount = document.getElementById("rowCount");
const colCount = document.getElementById("colCount");

const previewTable = document.getElementById("previewTable");
const previewSection = document.getElementById("previewSection");
const toggleBtn = document.getElementById("togglePreviewBtn");

const previewInput = document.getElementById("previewCount");

const table = document.getElementById("dataTable");

const missingEl = document.getElementById("missingCount");
const invalidEl = document.getElementById("invalidCount");
const totalEl = document.getElementById("totalIssues");

// Navigation
const navItems = document.querySelectorAll(".nav-item");
const pages = document.querySelectorAll(".page");
const pageTitle = document.getElementById("pageTitle");

// =========================================================
// Navigation Logic
// Handles active status and pages
// =========================================================


navItems.forEach(item => {

  item.addEventListener("click", () => {

    // Remove active state from all nav items
    navItems.forEach(nav => nav.classList.remove("active"));

    // Add active to clicked item
    item.classList.add("active");

    // Hide all pages
    pages.forEach(page => {
      page.classList.remove("active-page");
    });

    // Get target page
    const pageName = item.dataset.page;

    // Show matching page
    const activePage = document.getElementById(`${pageName}-page`);

    if (activePage) {
      activePage.classList.add("active-page");
    }

    // Update header title
    pageTitle.textContent = item.textContent;
  });

});



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
// FILE HANDLING PIPELINE
// Reads file → parses → sanitizes → analyzes → renders UI
// =========================================================
function handleFile(file) {

  // Reset preview rows
  previewInput.value = 10;

  spinner.classList.remove("hidden");

  const reader = new FileReader();

  reader.onload = e => {
    try {
      const data = new Uint8Array(e.target.result);

      // Parse Excel/CSV
      const wb = XLSX.read(data, { type: "array", cellFormula: false });
      const sheet = wb.Sheets[wb.SheetNames[0]];

      let json = XLSX.utils.sheet_to_json(sheet, {
        header: 1,
        defval: "" // preserve empty cells
      });

      // Data pipeline
      json = sanitize(json);
      const result = analyze(json);

      // Store for dynamic preview updates
      window.__lastData = result.flagged;

      // UI updates
      updateUI(file, result);
      renderPreview(result.flagged);
      renderTable(result.flagged);

      spinner.classList.add("hidden");

    } catch {
      errorMsg.textContent = "Error reading file.";
      spinner.classList.add("hidden");
    }
  };

  reader.readAsArrayBuffer(file);
}

// =========================================================
// SANITIZATION
// Prevents formula injection + HTML injection
// =========================================================
function sanitize(data) {
  return data.map(r =>
    r.map(c => {
      if (typeof c === "string") {
        if (/^[=+\-@]/.test(c)) return "'" + c;
        return c.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      }
      return c;
    })
  );
}

// =========================================================
// DATA ANALYSIS
// Classifies cells as:
// - missing
// - invalid (non-numeric)
// - normal
// =========================================================
function analyze(data) {
  let missing = 0, invalid = 0;

  const flagged = data.map(row =>
    row.map(cell => {
      if (cell === "" || cell == null) {
        missing++;
        return { value: "", type: "missing" };
      }

      if (isNaN(parseFloat(cell))) {
        invalid++;
        return { value: cell, type: "invalid" };
      }

      return { value: cell, type: "normal" };
    })
  );

  return { flagged, missing, invalid, total: missing + invalid };
}

// =========================================================
// UI UPDATE (summary panel)
// =========================================================
function updateUI(file, r) {
  fileSummary.classList.remove("hidden");

  fileName.textContent = "NAME: " + file.name;
  fileSize.textContent = "SIZE: " + (file.size / 1024).toFixed(1) + " KB";

  rowCount.textContent = r.flagged.length - 1;
  colCount.textContent = r.flagged[0]?.length || 0;

  missingEl.textContent = r.missing;
  invalidEl.textContent = r.invalid;
  totalEl.textContent = r.total;
}

// =========================================================
// PREVIEW HEIGHT MANAGEMENT (smooth animation)
// =========================================================
function updatePreviewHeight() {
  if (previewSection.classList.contains("preview-expanded")) {
    previewSection.style.maxHeight = previewSection.scrollHeight + "px";
  }
}

// =========================================================
// PREVIEW RENDERING (limited rows)
// =========================================================
function renderPreview(data) {
  previewTable.innerHTML = "";

  const count = Number(previewInput.value);
  const safeCount = Number.isNaN(count) ? 10 : count;

  data.slice(0, safeCount).forEach((row, i) => {
    const tr = document.createElement("tr");

    row.forEach(c => {
      const el = document.createElement(i === 0 ? "th" : "td");
      el.textContent = c.value;

      if (c.type === "missing") el.classList.add("cell-missing");
      if (c.type === "invalid") el.classList.add("cell-invalid");

      tr.appendChild(el);
    });

    previewTable.appendChild(tr);
  });

  updatePreviewHeight();
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




//////////////////////////////////////////
// Send data to backend
///////////////////////////////////////
document.getElementById("sendBtn").addEventListener("click", async () => {
  console.log("sending..." );
  const data = window.__lastData;
  // console.log("contents: " + data);

  // console.log("JSON contents: " + JSON.stringify(data));



  // Clean it RIGHT before sending
  const cleanData = data.map(row =>
    Array.isArray(row)
      ? row.map(Number)
      : Object.values(row).map(Number)
  );

  console.log("contents: " + cleanData)

  const response = await fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "text/csv"
    },
    body: cleanData
  });

  const result = await response.json();

  // console.log(result);
});