const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const handle = document.getElementById("handle");

menuToggle.addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
});

document.addEventListener("click", (e) => {
  if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
    sidebar.classList.add("collapsed");
  }
});

sidebar.addEventListener("click", (e) => {
  e.stopPropagation();
});

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

