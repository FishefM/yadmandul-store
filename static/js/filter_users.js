document
  .getElementById("mostrarActivos")
  .addEventListener("change", function () {
    let filasActivas = document.querySelectorAll(".activo");
    for (let i = 0; i < filasActivas.length; i++) {
      filasActivas[i].style.display = this.checked ? "" : "none";
    }
  });

document
  .getElementById("mostrarInactivos")
  .addEventListener("change", function () {
    let filasInactivas = document.querySelectorAll(".inactivo");
    for (let i = 0; i < filasInactivas.length; i++) {
      filasInactivas[i].style.display = this.checked ? "" : "none";
    }
  });
