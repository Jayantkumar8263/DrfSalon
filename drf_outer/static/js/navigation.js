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

        const token =
            localStorage.getItem(
                "authToken"
            );

        if (token) {
            if (guestLinks) {
                guestLinks.hidden = true;
            }

            if (userLinks) {
                userLinks.hidden = false;
            }

            checkAdminUser(token);
        } else {
            if (guestLinks) {
                guestLinks.hidden = false;
            }

            if (userLinks) {
                userLinks.hidden = true;
            }
        }

        async function checkAdminUser(
            authToken
        ) {
            try {
                const response =
                    await fetch(
                        "/api/appointments/",
                        {
                            method: "GET",
                            headers: {
                                "Authorization":
                                    `Token ${authToken}`,
                            },
                        }
                    );

                if (
                    response.status === 401
                ) {
                    localStorage.removeItem(
                        "authToken"
                    );

                    if (guestLinks) {
                        guestLinks.hidden =
                            false;
                    }

                    if (userLinks) {
                        userLinks.hidden =
                            true;
                    }

                    return;
                }

                if (
                    response.ok &&
                    adminLink
                ) {
                    /*
                     * A successful response alone
                     * does not prove the user is admin.
                     *
                     * The admin link is hidden by
                     * default and can be shown only
                     * if your login response includes
                     * is_staff.
                     */
                }
            } catch (error) {
                console.error(
                    "Unable to check user:",
                    error
                );
            }
        }

        if (
            menuToggle &&
            navLinks
        ) {
            menuToggle.addEventListener(
                "click",
                () => {
                    const isOpen =
                        navLinks.classList
                            .toggle("nav-open");

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
                () => {
                    localStorage.removeItem(
                        "authToken"
                    );

                    window.location.href =
                        "/";
                }
            );
        }
    }
);