"use strict";

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const message = document.querySelector(
            "#admin-message"
        );

        const container = document.querySelector(
            "#admin-appointments-container"
        );

        const statusFilter =
            document.querySelector(
                "#status-filter"
            );

        const orderingSelect =
            document.querySelector(
                "#ordering-select"
            );

        const token = localStorage.getItem(
            "authToken"
        );

        if (!token) {
            message.textContent =
                "Please login as admin to view this page.";

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

        function buildQueryParams() {
            const params = new URLSearchParams();

            if (statusFilter.value) {
                params.set(
                    "status",
                    statusFilter.value
                );
            }

            if (orderingSelect.value) {
                params.set(
                    "ordering",
                    orderingSelect.value
                );
            }

            return params.toString();
        }

        async function loadAppointments() {
            message.textContent =
                "Loading appointments...";

            message.className =
                "form-message";

            try {
                const queryString =
                    buildQueryParams();

                const url = queryString
                    ? `/api/appointments/?${queryString}`
                    : "/api/appointments/";

                const response = await fetch(
                    url,
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

        function createStatusBadge(status) {
            const badge =
                document.createElement("span");

            badge.className =
                `status-badge status-${status}`;

            badge.textContent = status;

            return badge;
        }

        function createActionButton(
            label,
            action,
            appointmentId,
            variant = "primary"
        ) {
            const button =
                document.createElement("button");

            button.className = `btn btn-${variant}`;
            button.textContent = label;

            button.addEventListener(
                "click",
                () => {
                    action(appointmentId);
                }
            );

            return button;
        }

        function createAppointmentRow(
            appointment
        ) {
            const row =
                document.createElement("div");

            row.className =
                "admin-appointment-row";

            const details =
                document.createElement("div");

            details.className =
                "appointment-details";

            const header =
                document.createElement("div");

            header.className =
                "appointment-header";

            header.appendChild(
                createStatusBadge(
                    appointment.status
                )
            );

            const serviceTitle =
                document.createElement("h3");

            serviceTitle.textContent =
                appointment.service_name;

            header.appendChild(serviceTitle);

            details.appendChild(header);

            const customerText =
                document.createElement("p");

            customerText.textContent =
                `Customer: ${
                    appointment.customer_name ||
                    "Unknown"
                }`;

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

            details.appendChild(customerText);
            details.appendChild(staffText);
            details.appendChild(dateText);
            details.appendChild(timeText);
            details.appendChild(notesText);

            row.appendChild(details);

            const actions =
                document.createElement("div");

            actions.className =
                "appointment-actions";

            if (
                appointment.status === "pending"
            ) {
                actions.appendChild(
                    createActionButton(
                        "Confirm",
                        confirmAppointment,
                        appointment.id,
                        "primary"
                    )
                );
            }

            if (
                appointment.status === "confirmed"
            ) {
                actions.appendChild(
                    createActionButton(
                        "Complete",
                        completeAppointment,
                        appointment.id,
                        "success"
                    )
                );
            }

            if (
                appointment.status === "pending" ||
                appointment.status === "confirmed"
            ) {
                actions.appendChild(
                    createActionButton(
                        "Cancel",
                        cancelAppointment,
                        appointment.id,
                        "outline"
                    )
                );
            }

            row.appendChild(actions);

            return row;
        }

        function renderAppointments(
            appointments
        ) {
            message.textContent = "";

            if (
                appointments.length === 0
            ) {
                message.textContent =
                    "No appointments found.";

                message.className =
                    "form-message form-message-warning";

                return;
            }

            container.innerHTML = "";

            appointments.forEach(
                (appointment) => {
                    container.appendChild(
                        createAppointmentRow(
                            appointment
                        )
                    );
                }
            );
        }

        async function callStatusAction(
            urlPath,
            appointmentId,
            successMessage
        ) {
            message.textContent =
                "Processing...";

            message.className =
                "form-message";

            try {
                const response = await fetch(
                    `/api/appointments/${appointmentId}/${urlPath}/`,
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
                        "Action failed."
                    );
                }

                message.textContent =
                    successMessage;

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

        function confirmAppointment(
            appointmentId
        ) {
            callStatusAction(
                "confirm",
                appointmentId,
                "Appointment confirmed."
            );
        }

        function completeAppointment(
            appointmentId
        ) {
            callStatusAction(
                "complete",
                appointmentId,
                "Appointment completed."
            );
        }

        function cancelAppointment(
            appointmentId
        ) {
            callStatusAction(
                "cancel",
                appointmentId,
                "Appointment cancelled."
            );
        }

        statusFilter.addEventListener(
            "change",
            loadAppointments
        );

        orderingSelect.addEventListener(
            "change",
            loadAppointments
        );

        loadAppointments();
    }
);