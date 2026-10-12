"use strict";

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const menuToggle =
            document.querySelector(
                "#menu-toggle"
            );

        const navLinks =
            document.querySelector(
                "#nav-links"
            );

        const guestLinks =
            document.querySelector(
                "#guest-links"
            );

        const userLinks =
            document.querySelector(
                "#user-links"
            );

        const adminLink =
            document.querySelector(
                "#admin-link"
            );

        const logoutButton =
            document.querySelector(
                "#logout-button"
            );

        const appointmentsLink =
            document.querySelector(
                "#appointments-link"
            );

        const token =
            localStorage.getItem(
                "authToken"
            );

        const storedUser =
            localStorage.getItem(
                "currentUser"
            );

        let currentUser = null;

        if (storedUser) {
            try {
                currentUser = JSON.parse(
                    storedUser
                );
            } catch (error) {
                localStorage.removeItem(
                    "currentUser"
                );
            }
        }

        function showGuestNavigation() {
            if (guestLinks) {
                guestLinks.hidden = false;
            }

            if (userLinks) {
                userLinks.hidden = true;
            }

            if (adminLink) {
                adminLink.hidden = true;
            }
        }

        function showUserNavigation(user) {
            if (guestLinks) {
                guestLinks.hidden = true;
            }

            if (userLinks) {
                userLinks.hidden = false;
            }

            if (adminLink) {
                adminLink.hidden =
                    !user.is_staff;
            }
        }

        function logoutUser() {
            localStorage.removeItem(
                "authToken"
            );

            localStorage.removeItem(
                "currentUser"
            );

            window.location.href = "/";
        }

        if (token && currentUser) {
            showUserNavigation(currentUser);
        } else {
            showGuestNavigation();
        }

        if (appointmentsLink) {
            appointmentsLink.addEventListener(
                "click",
                (event) => {
                    if (!token) {
                        event.preventDefault();

                        window.location.href =
                            "/login/";
                    }
                }
            );
        }

        if (
            menuToggle &&
            navLinks
        ) {
            menuToggle.addEventListener(
                "click",
                () => {
                    const isOpen =
                        navLinks.classList.toggle(
                            "nav-open"
                        );

                    menuToggle.setAttribute(
                        "aria-expanded",
                        String(isOpen)
                    );
                }
            );
        }

        if (logoutButton) {
            logoutButton.addEventListener(
                "click",
                logoutUser
            );
        }
    }
);