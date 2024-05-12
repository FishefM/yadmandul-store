import filter_users from "./filter_users.js";

document.addEventListener("DOMContentLoaded", () => {
  filter_users(
    "mostrarActivos_prod",
    "mostrarInactivos_prod",
    "buscar_prod",
    "data-nombre-prod"
  );
});
