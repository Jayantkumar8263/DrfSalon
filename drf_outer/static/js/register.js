"use strict";

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const form =
            document.querySelector(
                "#register-form"
            );

        if (!form) {
            return;
        }

        const message =
            document.querySelector(
                "#register-message"
            );

        const usernameInput =
            document.querySelector(
                "#register-username"
            );

        const emailInput =
            document.querySelector(
                "#register-email"
            );

        const passwordInput =
            document.querySelector(
                "#register-password"
            );

        const submitButton =
            form.querySelector(
                'button[type="submit"]'
            );

        function showMessage(
            text,
            type
        ) {
            if (!message) {
                return;
            }

            message.textContent = text;
            message.className =
                `form-message ${type}`;
        }

        function getErrorMessage(data) {
            if (!data) {
                return "Registration failed.";
            }

            if (typeof data.detail === "string") {
                return data.detail;
            }

            const errors = [];

            for (const [field, value] of
                Object.entries(data)) {
                const text = Array.isArray(value)
                    ? value.join(" ")
                    : String(value);

                if (field === "non_field_errors") {
                    errors.push(text);
                } else {
                    errors.push(
                        `${field}: ${text}`
                    );
                }
            }

            return errors.join(" ") ||
                "Registration failed.";
        }

        form.addEventListener(
            "submit",
            async (event) => {
                event.preventDefault();

                const username =
                    usernameInput.value.trim();

                const email =
                    emailInput.value.trim();

                const password =
                    passwordInput.value;

                if (
                    !username ||
                    !email ||
                    !password
                ) {
                    showMessage(
                        "Please fill in all fields.",
                        "form-message-error"
                    );

                    return;
                }

                if (submitButton) {
                    submitButton.disabled = true;
                    submitButton.textContent =
                        "Creating account...";
                }

                showMessage(
                    "Creating your account...",
                    ""
                );

                try {
                    const response = await fetch(
                        "/api/register/",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                username: usernameInput.value.trim(),
                                email: emailInput.value.trim(),
                                password: passwordInput.value,
                            }),
                        }
                    );

                    const contentType =
                        response.headers.get(
                            "content-type"
                        ) || "";

                    let data = null;

                    if (
                        contentType.includes(
                            "application/json"
                        )
                    ) {
                        data =
                            await response.json();
                    } else {
                        const responseText =
                            await response.text();

                        if (!response.ok) {
                            throw new Error(
                                `Server returned HTTP ${response.status}. ` +
                                "Check the Django terminal for the error."
                            );
                        }

                        throw new Error(
                            "The server returned HTML instead of JSON. " +
                            "Check the registration API URL and Django logs."
                        );
                    }

                    if (!response.ok) {
                        throw new Error(
                            getErrorMessage(data)
                        );
                    }

                    /*
                     * Store credentials only if the
                     * registration API returns them.
                     * If it does not, the user will
                     * proceed to the login page.
                     */
                    if (data.token) {
                        localStorage.setItem(
                            "authToken",
                            data.token
                        );
                    }

                    if (data.user) {
                        localStorage.setItem(
                            "currentUser",
                            JSON.stringify(data.user)
                        );
                    }

                    showMessage(
                        "Registration successful. Please log in.",
                        "form-message-success"
                    );

                    form.reset();

                    window.setTimeout(() => {
                        window.location.href =
                            "/";
                    }, 700);
                } catch (error) {
                    showMessage(
                        error.message,
                        "form-message-error"
                    );
                } finally {
                    if (submitButton) {
                        submitButton.disabled = false;
                        submitButton.textContent =
                            "Create account";
                    }
                }
            }
        );
    }
);