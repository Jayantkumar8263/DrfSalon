"use strict";

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const message =
            document.querySelector(
                "#profile-message"
            );

        const profileCard =
            document.querySelector(
                "#profile-card"
            );

        const usernameElement =
            document.querySelector(
                "#profile-username"
            );

        const emailElement =
            document.querySelector(
                "#profile-email"
            );

        const roleElement =
            document.querySelector(
                "#profile-role"
            );

        const initialElement =
            document.querySelector(
                "#profile-initial"
            );

        const logoutButton =
            document.querySelector(
                "#profile-logout-button"
            );

        const token =
            localStorage.getItem(
                "authToken"
            );

        const storedUser =
            localStorage.getItem(
                "currentUser"
            );

        if (!token || !storedUser) {
            window.location.href =
                "/login/";

            return;
        }

        let user;

        try {
            user = JSON.parse(storedUser);
        } catch (error) {
            localStorage.removeItem(
                "authToken"
            );

            localStorage.removeItem(
                "currentUser"
            );

            window.location.href =
                "/login/";

            return;
        }

        usernameElement.textContent =
            user.username || "Customer";

        emailElement.textContent =
            user.email || "No email provided";

        roleElement.textContent =
            user.is_staff
                ? "Salon administrator"
                : "Customer account";

        initialElement.textContent =
            (
                user.username || "U"
            )
                .charAt(0)
                .toUpperCase();

        message.textContent = "";

        profileCard.hidden = false;

        logoutButton.addEventListener(
            "click",
            () => {
                localStorage.removeItem(
                    "authToken"
                );

                localStorage.removeItem(
                    "currentUser"
                );

                window.location.href = "/";
            }
        );
    }
);