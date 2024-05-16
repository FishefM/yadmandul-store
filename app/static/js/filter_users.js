export default function filter_users(activos, inactivos, buscar, data) {
  if (activos) {
    document.getElementById(activos).addEventListener("change", function () {
      let filasActivas = document.querySelectorAll(".activo");
      for (let i = 0; i < filasActivas.length; i++) {
        filasActivas[i].style.display = this.checked ? "" : "none";
      }
    });
  }
  if (inactivos) {
    document.getElementById(inactivos).addEventListener("change", function () {
      let filasInactivas = document.querySelectorAll(".inactivo");
      for (let i = 0; i < filasInactivas.length; i++) {
        filasInactivas[i].style.display = this.checked ? "" : "none";
      }
    });
  }
  if (buscar) {
    document.getElementById(buscar).addEventListener("input", function () {
      let buscar = this.value.toLowerCase();
      let filas = document.querySelectorAll(`tr[${data}]`);
      for (let i = 0; i < filas.length; i++) {
        let nombre = filas[i].getAttribute(data).toLowerCase();
        filas[i].style.display = nombre.includes(buscar) ? "" : "none";
      }
    });
  }
}
