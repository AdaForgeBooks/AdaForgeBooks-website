const menuButton = document.querySelector(".menu-button");
const navigation = document.querySelector(".main-navigation");

if (menuButton && navigation) {
    menuButton.addEventListener("click", () => {
        const open = navigation.classList.toggle("is-open");
        menuButton.setAttribute("aria-expanded", String(open));
    });

    navigation.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            navigation.classList.remove("is-open");
            menuButton.setAttribute("aria-expanded", "false");
        });
    });
}
