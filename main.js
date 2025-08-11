const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const handle = document.getElementById("handle");

// Toggle sidebar when menu button is clicked
menuToggle.addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
});

// Toggle sidebar when clicking anywhere on the screen (except sidebar and menu button)
document.addEventListener("click", (e) => {
  // Don't collapse if clicking on sidebar, menu button, or their children
  if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
    sidebar.classList.add("collapsed");
  }
});

// Prevent sidebar from collapsing when clicking inside it
sidebar.addEventListener("click", (e) => {
  e.stopPropagation();
});

// Prevent menu button clicks from triggering document click
menuToggle.addEventListener("click", (e) => {
  e.stopPropagation();
});

const resize = (e) => {
  let newWidth = e.clientX - sidebar.offsetLeft;

  if (newWidth < 54) newWidth = 54;

  sidebar.style.width = `${newWidth}px`;
};

const stopResize = (e) => {
  window.removeEventListener("mousemove", resize);
  window.removeEventListener("mouseup", stopResize);
};

const initResize = () => {
  window.addEventListener("mousemove", resize);
  window.addEventListener("mouseup", stopResize);
};

handle.addEventListener("mousedown", initResize);

