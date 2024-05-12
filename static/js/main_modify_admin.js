import modify from "./modify_data.js";

document.addEventListener("DOMContentLoaded", () => {
  modify("form-modify_photo_admin", "/upload_img_admin");
  modify("form-modify_name_admin", "/modify_name_admin");
  modify("form-modify_appat_admin", "/modify_appat_admin");
  modify("form-modify_apmat_admin", "/modify_apmat_admin");
  modify("form-modify_correo_admin", "/modify_correo_admin");
  modify("form-modify_password_admin", "/modify_password_admin");
  modify("form-insert_proveedores", "/insert_proveedores");
});
