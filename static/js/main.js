import filterCards from "./filter_cards.js";

document.addEventListener("DOMContentLoaded", () => {
  filterCards("card-filter-bebidas", ".bebidas");
  filterCards("card-filter-dulces", ".dulces");
});
