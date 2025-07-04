document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("searchInput");
    const cards = document.querySelectorAll(".card");

    if (input) {
        input.addEventListener("input", () => {
            const val = input.value.toLowerCase();
            cards.forEach(card => {
                const name = card.getAttribute("data-name");
                card.style.display = name.includes(val) ? "block" : "none";
            });
        });
    }
});
