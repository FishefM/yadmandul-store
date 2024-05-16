export default function modify(form, action) {
  const $avisoExito = document.querySelector(".aviso-exito");
  const $pAvisoExito = document.querySelector(".aviso-exito p");
  const $avisoFracaso = document.querySelector(".aviso-fracaso");
  const $pAvisoFracaso = document.querySelector(".aviso-fracaso p");
  const $closeAvisoExito = document.getElementById("close-aviso-exito");
  const $closeAvisoFracaso = document.getElementById("close-aviso-fracaso");

  $closeAvisoExito.addEventListener("click", (e) => {
    $avisoExito.classList.remove("visible");
    window.location.reload();
  });

  $closeAvisoFracaso.addEventListener("click", (e) => {
    $avisoFracaso.classList.remove("visible");
  });

  document.getElementById(form).addEventListener("submit", function (e) {
    e.preventDefault();

    fetch(action, {
      method: "POST",
      body: new FormData(this),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.modificacion_exitosa) {
          if (data.info) $pAvisoExito.textContent = data.info;
          $avisoExito.classList.add("visible");
        } else {
          $pAvisoFracaso.textContent =
            "Error en la actualización: " + data.error;
          $avisoFracaso.classList.add("visible");
        }
        window.scrollTo(0, 0);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
}
