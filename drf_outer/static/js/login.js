"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#login-form");

    if (!form) {
        return;
    }

    const usernameInput = document.querySelector(
        "#username"
    );

    const passwordInput = document.querySelector(
        "#password"
    );

    const submitButton = document.querySelector(
        "#login-submit"
    );

    const message = document.querySelector(
        "#login-message"
    );

    function showMessage(
        text,
        type = ""
    ) {
        message.textContent = text;
        message.className =
            `form-message ${type}`;
    }

    form.addEventListener(
        "submit",
        async (event) => {
            event.preventDefault();

            const username = usernameInput.value.trim();
            const password = passwordInput.value;

            if (!username || !password) {
                showMessage(
                    "Username and password are required.",
                    "form-message-error"
                );

                return;
            }

            submitButton.disabled = true;
            submitButton.textContent = "Logging in...";
            showMessage("");

            try {
                const response = await fetch(
                    "/api/login/",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json",
                        },
                        body: JSON.stringify({
                            username: username,
                            password: password,
                        }),
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.non_field_errors?.join(
                            " "
                        ) ||
                        data.detail ||
                        "Invalid username or password."
                    );
                }

                localStorage.setItem(
                    "authToken",
                    data.token
                );
                localStorage.setItem(
                    "currentUser",
                    JSON.stringify(data.user)
                );
                showMessage(
                    "Login successful. Redirecting...",
                    "form-message-success"
                );

                window.setTimeout(() => {
                    if (data.user.is_staff) {
                        window.location.href =
                            "/admin-dashboard/";
                    } else {
                        window.location.href =
                            "/";
                    }
                }, 700);
            } catch (error) {
                showMessage(
                    error.message,
                    "form-message-error"
                );
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = "Login";
            }
        }
    );
});