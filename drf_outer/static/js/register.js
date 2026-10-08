"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(
        "#register-form"
    );

    if (!form) {
        return;
    }

    const message = document.querySelector(
        "#register-message"
    );

    form.addEventListener(
        "submit",
        async (event) => {
            event.preventDefault();

            const username = document.querySelector(
                "#register-username"
            ).value.trim();

            const email = document.querySelector(
                "#register-email"
            ).value.trim();

            const password = document.querySelector(
                "#register-password"
            ).value;

            try {
                const response = await fetch(
                    "/api/register/",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json",
                        },
                        body: JSON.stringify({
                            username: username,
                            email: email,
                            password: password,
                        }),
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.username?.join(" ") ||
                        data.password?.join(" ") ||
                        data.detail ||
                        "Registration failed."
                    );
                }

                message.textContent =
                    "Registration successful. Please login.";

                message.className =
                    "form-message form-message-success";

                form.reset();

                window.setTimeout(() => {
                    window.location.href =
                        "/login/";
                }, 900);
            } catch (error) {
                message.textContent =
                    error.message;

                message.className =
                    "form-message form-message-error";
            }
        }
    );
});