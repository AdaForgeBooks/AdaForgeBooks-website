document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".afb-header").forEach(header => {
        const button = header.querySelector(".afb-menu-button");

        if (!button) return;

        button.addEventListener("click", () => {
            const open = header.classList.toggle("menu-open");

            button.setAttribute("aria-expanded", String(open));
            button.setAttribute(
                "aria-label",
                open ? "Close menu" : "Open menu"
            );
        });
    });
});
