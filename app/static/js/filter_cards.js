export default function filterCards(inputSearch, selector) {
  const $inputSearch = document.getElementById(inputSearch);
  const $selector = document.querySelectorAll(selector);

  $inputSearch.addEventListener("keyup", (e) => {
    e.target.value = e.target.value.toLowerCase();
    $selector.forEach((el) => {
      el.textContent.toLowerCase().includes(e.target.value)
        ? el.classList.remove("filter")
        : el.classList.add("filter");
    });
  });
}
