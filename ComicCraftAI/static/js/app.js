const form =
    document.getElementById("comic-form");

const button =
    document.getElementById(
        "generate-button"
    );


if (form && button) {

    form.addEventListener(
        "submit",
        () => {

            button.disabled = true;

            const text =
                button.querySelector("span");

            if (text) {
                text.textContent =
                    "Generating your comic...";
            }

            button.style.opacity = "0.7";
        }
    );
}