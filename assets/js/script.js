// ===== SCRIPT.JS - JavaScript chung =====

// Toggle Sidebar
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebarOverlay");
  if (sidebar) sidebar.classList.toggle("show");
  if (overlay) overlay.classList.toggle("show");
}

// Dong sidebar khi click overlay
document.addEventListener("DOMContentLoaded", function () {
  const overlay = document.getElementById("sidebarOverlay");
  if (overlay) {
    overlay.addEventListener("click", toggleSidebar);
  }

  // Auto hide alerts
  setTimeout(function () {
    document.querySelectorAll(".alert.auto-hide").forEach(function (el) {
      const bsAlert = new bootstrap.Alert(el);
      bsAlert.close();
    });
  }, 5000);

  // Init Bootstrap tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // Dong ho thoi gian
  updateClock();
  setInterval(updateClock, 1000);

  // Preview anh khi upload
  const imgInputs = document.querySelectorAll('input[type="file"][data-preview]');
  imgInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      const previewId = this.getAttribute("data-preview");
      const preview = document.getElementById(previewId);
      if (preview && this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) { preview.src = e.target.result; };
        reader.readAsDataURL(this.files[0]);
      }
    });
  });

  // Active sidebar link
  setActiveSidebarLink();
});

// Dong ho
function updateClock() {
  const el = document.getElementById("currentTime");
  if (el) {
    const now = new Date();
    const days = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];
    const d = days[now.getDay()];
    const time = now.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
    const date = now.toLocaleDateString("vi-VN");
    el.textContent = d + " " + date + " - " + time;
  }
}

// Set active sidebar
function setActiveSidebarLink() {
  const path = window.location.pathname;
  document.querySelectorAll(".sidebar-nav .nav-link").forEach(function (link) {
    const href = link.getAttribute("href");
    if (href && path.endsWith(href.split("/").pop())) {
      link.classList.add("active");
    }
  });
}

// Xac nhan xoa
function confirmDelete(url, name) {
  if (confirm("Ban co chac chan muon xoa \"" + name + "\"?\nHanh dong nay khong the hoan tac!")) {
    window.location.href = url;
  }
}

// Format tien te VND
function formatMoney(amount) {
  return new Intl.NumberFormat("vi-VN").format(amount) + " d";
}

// Tinh toan hoa don tu dong
function calcInvoiceTotal() {
  const fields = ["tien_phong", "tien_dien", "tien_nuoc", "tien_dich_vu", "phi_khac"];
  let total = 0;
  fields.forEach(function (id) {
    const el = document.getElementById(id);
    if (el) total += parseFloat(el.value) || 0;
  });
  const totalEl = document.getElementById("tong_tien");
  if (totalEl) totalEl.value = total;
  const displayEl = document.getElementById("tong_tien_display");
  if (displayEl) displayEl.textContent = formatMoney(total);
}

// Tim kiem live
function liveSearch(inputId, tableId) {
  const input = document.getElementById(inputId);
  const table = document.getElementById(tableId);
  if (!input || !table) return;
  input.addEventListener("keyup", function () {
    const filter = this.value.toLowerCase();
    table.querySelectorAll("tbody tr").forEach(function (row) {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(filter) ? "" : "none";
    });
  });
}

// Reset form modal khi dong
document.addEventListener("hidden.bs.modal", function (e) {
  const form = e.target.querySelector("form");
  if (form) form.reset();
  const alerts = e.target.querySelectorAll(".alert");
  alerts.forEach(function (a) { a.remove(); });
});