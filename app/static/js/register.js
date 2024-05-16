window.addEventListener("load", (event) => {
  const $avisoExito = document.querySelector(".aviso-exito");
  const $closeAvisoExito = document.getElementById("close-aviso-exito");
  const $btnLogin = document.getElementById("btn-login");
  const $closeAvisoFracaso = document.getElementById("close-aviso-fracaso");
  const $avisoFracaso = document.querySelector(".aviso-fracaso");
  const $pAvisoFracaso = document.querySelector(".aviso-fracaso p");
  $closeAvisoExito.addEventListener("click", () => {
    $avisoExito.classList.toggle("visible");
    $btnLogin.click();
  });
  $closeAvisoFracaso.addEventListener("click", () =>
    $avisoFracaso.classList.toggle("visible")
  );
  document
    .getElementById("form-register")
    .addEventListener("submit", function (e) {
      e.preventDefault();

      fetch("/add_usr", {
        method: "POST",
        body: new FormData(this),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.registro_exitoso) {
            $avisoExito.classList.toggle("visible");
            // alert("Registro exitoso!");
            // window.location.reload();
          } else {
            // alert("Error en el registro: " + data.error);

            $pAvisoFracaso.textContent = "Error en el registro: " + data.error;
            $avisoFracaso.classList.toggle("visible");
          }
          window.scrollTo(0, 0);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
});
