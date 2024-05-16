import modify from "./modify_data.js";

document.addEventListener("DOMContentLoaded", () => {
  modify("form-modify_name_employee", "/modify_name_employee");
  modify("form-modify_appat_employee", "/modify_appat_employee");
  modify("form-modify_apmat_employee", "/modify_apmat_employee");
  modify("form-modify_correo_employee", "/modify_correo_employee");
  modify("form-modify_password_employee", "/modify_password_employee");
  modify("form-modify_photo_employee", "/upload_img_employee");
  modify("form-insert_products", "/insert_products");
  modify("form-modify_fechanac_employee", "/modify_fechanac_employee");
});
