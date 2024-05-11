import filter_users from "./filter_users.js";

document.addEventListener("DOMContentLoaded", () => {
  filter_users(
    "mostrarActivos_employees",
    "mostrarInactivos_employees",
    "buscar_employees",
    "data-nombre-emp"
  );
  filter_users(
    "mostrarActivos_cli",
    "mostrarInactivos_cli",
    "buscar_cli",
    "data-nombre-cli"
  );
});
