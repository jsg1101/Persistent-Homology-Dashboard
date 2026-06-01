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

      document.body.scrollTo({
        top: 0,
        behavior: "smooth"
    });
  
      // Update header title
      pageTitle.textContent = item.textContent;
    });
  
  });