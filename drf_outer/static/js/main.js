"use strict";

document.addEventListener("DOMContentLoaded", () => {
    console.log("main.js loaded successfully");

    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach((link) => {
        const linkPath = new URL(
            link.href,
            window.location.origin
        ).pathname;

        if (linkPath === currentPath) {
            link.classList.add("active");
        }
    });

    const menuButton = document.querySelector(".menu-toggle");
    const navLinksContainer = document.querySelector(".nav-links");

    if (menuButton && navLinksContainer) {
        menuButton.addEventListener("click", () => {
            navLinksContainer.classList.toggle("nav-open");
        });
    }

    const bookingButtons = document.querySelectorAll(
        "[data-book-service]"
    );

    bookingButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const serviceName = button.dataset.bookService;

            console.log(
                `Booking selected for: ${serviceName}`
            );

            const bookingUrl = button.dataset.bookingUrl;

            if (bookingUrl) {
                window.location.href = bookingUrl;
            }
        });
    });

    const messages = document.querySelectorAll(
        ".alert, .message"
    );

    messages.forEach((message) => {
        const closeButton = message.querySelector(
            ".message-close"
        );

        if (closeButton) {
            closeButton.addEventListener("click", () => {
                message.remove();
            });
        }
    });
});