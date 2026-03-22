document.addEventListener("DOMContentLoaded", () => {
  const flashContainer = document.querySelector("[data-auto-dismiss]");
  if (!flashContainer) return;
  window.setTimeout(() => {
    flashContainer.querySelectorAll(".alert").forEach((alert) => {
      alert.classList.add("fade");
      alert.classList.remove("show");
    });
  }, 4000);
});
