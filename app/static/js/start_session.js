window.addEventListener("load", (event) => {
  const $avisoPassword = document.querySelector(".aviso-password");
  const $closeAvisoPassword = document.getElementById("close-aviso-password");
  const $pAvisoPassword = document.querySelector(".aviso-password p");

  $closeAvisoPassword.addEventListener("click", (e) => {
    $avisoPassword.classList.toggle("visible");
  });
  document
    .getElementById("form-start-session")
    .addEventListener("submit", function (e) {
      e.preventDefault();

      fetch("/startsession", {
        method: "POST",
        body: new FormData(this),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.loggeo_exitoso) {
            if (data.user === "cliente") window.location.href = "/";
            else if (data.user === "empleado")
              window.location.href = "/empleados";
            else if (data.user === "administrador")
              window.location.href = "/administradores";
            // alert("Registro exitoso!");
            // window.location.reload();
          } else {
            // alert("Error en el registro: " + data.error);
            if (data.error) $pAvisoPassword.textContent = data.error;
            $avisoPassword.classList.toggle("visible");
          }
          window.scrollTo(0, 0);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
});
