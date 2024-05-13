import modify from "./modify_data.js";

document.addEventListener("DOMContentLoaded", () => {
  modify("form-modify_photo_client", "/upload_img_client");
  modify("form-modify_name_cli", "/modify_name_cli");
  modify("form-modify_appat_cli", "/modify_appat_cli");
  modify("form-modify_apmat_cli", "/modify_apmat_cli");
  modify("form-modify_correo_cli", "/modify_correo_cli");
  modify("form-modify_password_cli", "/modify_password_cli");
});
