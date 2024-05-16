imgCard = document.querySelectorAll(".img-card");

imgCard.forEach((element) => {
  element.addEventListener("click", (e) => {
    //remove active class
    imgCard.forEach((el) => {
      el.classList.remove("active");
    });
    element.classList.add("active");
  });
});
