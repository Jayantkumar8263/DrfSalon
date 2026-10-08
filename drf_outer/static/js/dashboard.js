"use strict";

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const message = document.querySelector(
            "#dashboard-message"
        );

        const container = document.querySelector(
            "#appointments-container"
        );

        const token = localStorage.getItem(
            "authToken"
        );

        if (!token) {
            message.textContent =
                "Please login to view your appointments.";

            message.className =
                "form-message form-message-warning";

            window.setTimeout(() => {
                window.location.href =
                    "/login/";
            }, 1000);

            return;
        }

        function getHeaders() {
            return {
                "Authorization":
                    `Token ${token}`,
            };
        }

        async function loadAppointments() {
            try {
                const response = await fetch(
                    "/api/appointments/",
                    {
                        method: "GET",
                        headers: getHeaders(),
                    }
                );

                if (
                    response.status === 401 ||
                    response.status === 403
                ) {
                    localStorage.removeItem(
                        "authToken"
                    );

                    window.location.href =
                        "/login/";

                    return;
                }

                const data =
                    await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.detail ||
                        "Unable to load appointments."
                    );
                }

                renderAppointments(data);
            } catch (error) {
                message.textContent =
                    error.message;

                message.className =
                    "form-message form-message-error";
            }
        }

        function createSafeText(value) {
            const element =
                document.createElement("span");

            element.textContent = value;

            return element;
        }

        function createStatusBadge(status) {
            const badge =
                document.createElement("span");

            badge.className =
                `status-badge status-${status}`;

            badge.textContent = status;

            return badge;
        }

        function createAppointmentCard(
            appointment
        ) {
            const card =
                document.createElement("article");

            card.className =
                "appointment-card";

            const details =
                document.createElement("div");

            const serviceTitle =
                document.createElement("h2");

            serviceTitle.textContent =
                appointment.service_name;

            const staffText =
                document.createElement("p");

            staffText.textContent =
                `Staff: ${
                    appointment.staff_name ||
                    "Any staff"
                }`;

            const dateText =
                document.createElement("p");

            dateText.textContent =
                `Date: ${appointment.appointment_date}`;

            const timeText =
                document.createElement("p");

            timeText.textContent =
                `Time: ${appointment.appointment_time}`;

            const notesText =
                document.createElement("p");

            notesText.textContent =
                `Notes: ${
                    appointment.notes ||
                    "No notes"
                }`;

            details.appendChild(
                createStatusBadge(
                    appointment.status
                )
            );

            details.appendChild(
                serviceTitle
            );

            details.appendChild(staffText);
            details.appendChild(dateText);
            details.appendChild(timeText);
            details.appendChild(notesText);

            card.appendChild(details);

            if (
                appointment.status ===
                    "pending" ||
                appointment.status ===
                    "confirmed"
            ) {
                const cancelButton =
                    document.createElement("button");

                cancelButton.className =
                    "btn btn-outline";

                cancelButton.textContent =
                    "Cancel booking";

                cancelButton.addEventListener(
                    "click",
                    () => {
                        cancelAppointment(
                            appointment.id
                        );
                    }
                );

                card.appendChild(
                    cancelButton
                );
            }

            return card;
        }

        function renderAppointments(
            appointments
        ) {
            message.textContent = "";

            if (
                appointments.length === 0
            ) {
                message.textContent =
                    "You do not have any appointments yet.";

                message.className =
                    "form-message form-message-warning";

                return;
            }

            container.innerHTML = "";

            appointments.forEach(
                (appointment) => {
                    container.appendChild(
                        createAppointmentCard(
                            appointment
                        )
                    );
                }
            );
        }

        async function cancelAppointment(
            appointmentId
        ) {
            message.textContent =
                "Cancelling appointment...";

            message.className =
                "form-message";

            try {
                const response =
                    await fetch(
                        `/api/appointments/${appointmentId}/cancel/`,
                        {
                            method: "POST",
                            headers: getHeaders(),
                        }
                    );

                const data =
                    await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.detail ||
                        "Unable to cancel appointment."
                    );
                }

                message.textContent =
                    "Appointment cancelled successfully.";

                message.className =
                    "form-message form-message-success";

                loadAppointments();
            } catch (error) {
                message.textContent =
                    error.message;

                message.className =
                    "form-message form-message-error";
            }
        }

        loadAppointments();
    }
);