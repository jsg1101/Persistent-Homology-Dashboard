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

  // force default radio states
  //  option card diagram
  document.querySelector('input[name="dimension_diagram"][value="1"]').checked = true;
  document.querySelector('input[name="metric_diagram"][value="0"]').checked = true;
  document.getElementById("prime_diagram").value = 2;
  //  option card barcodes
  document.querySelector('input[name="dimension_barcodes"][value="1"]').checked = true;
  document.querySelector('input[name="metric_barcodes"][value="0"]').checked = true;
  document.getElementById("prime_barcodes").value = 2;

});


// =========================================================
// DOM ELEMENT REFERENCES
// Centralized access to all UI elements
// =========================================================
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

const spinner = document.getElementById("spinner");
const errorMsg = document.getElementById("errorMsg");

// File Summary

const fileSummary = document.getElementById("fileSummary");

const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");

const rowCount = document.getElementById("rowCount");
const colCount = document.getElementById("colCount");

const missingEl = document.getElementById("missingCount");
const invalidEl = document.getElementById("invalidCount");
const totalEl = document.getElementById("totalIssues");

//File Preview

const previewTable = document.getElementById("previewTable");
const previewSection = document.getElementById("previewSection");
const toggleBtn = document.getElementById("togglePreviewBtn");

const previewInput = document.getElementById("previewCount");

const table = document.getElementById("dataTable");


const diagramCards = document.querySelectorAll("#diagrams-page .card");
const barcodeCards = document.querySelectorAll("#barcodes-page .card");


// Navigation
const navItems = document.querySelectorAll(".nav-item");
const pages = document.querySelectorAll(".page");
const pageTitle = document.getElementById("pageTitle");
















