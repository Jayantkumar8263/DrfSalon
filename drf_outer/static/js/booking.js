"use strict";

document.addEventListener(
    "DOMContentLoaded",
    () => {
        const form =
            document.querySelector(
                "#booking-form"
            );

        const serviceSelect =
            document.querySelector(
                "#service"
            );

        const staffSelect =
            document.querySelector(
                "#staff"
            );

        const dateInput =
            document.querySelector(
                "#appointment-date"
            );

        const timeSelect =
            document.querySelector(
                "#appointment-time"
            );

        const notesInput =
            document.querySelector(
                "#notes"
            );

        const message =
            document.querySelector(
                "#booking-message"
            );

        const submitButton =
            document.querySelector(
                "#booking-submit"
            );

        const token =
            localStorage.getItem(
                "authToken"
            );

        if (!token) {
            window.location.href =
                "/login/";

            return;
        }

        function showMessage(
            text,
            type = ""
        ) {
            message.textContent = text;

            message.className =
                `form-message ${type}`;
        }

        function authHeaders() {
            return {
                "Authorization":
                    `Token ${token}`,
                "Content-Type":
                    "application/json",
            };
        }

        function getSelectedServiceId() {
            const params =
                new URLSearchParams(
                    window.location.search
                );

            return params.get("service");
        }

        function resetTimeSelect(text) {
            timeSelect.innerHTML = "";

            const option =
                document.createElement(
                    "option"
                );

            option.value = "";
            option.textContent = text;

            timeSelect.appendChild(option);
        }

        function extractList(data) {
            return data.results || data;
        }

        async function loadServices() {
            const response =
                await fetch(
                    "/api/services/"
                );

            const data =
                await response.json();

            if (!response.ok) {
                throw new Error(
                    "Unable to load services."
                );
            }

            serviceSelect.innerHTML =
                '<option value="">Select a service</option>';

            const services =
                extractList(data);

            services.forEach((service) => {
                const option =
                    document.createElement(
                        "option"
                    );

                option.value = service.id;

                option.textContent =
                    `${service.name} - ₹${service.price}`;

                serviceSelect.appendChild(option);
            });

            const selectedServiceId =
                getSelectedServiceId();

            if (selectedServiceId) {
                const serviceOption =
                    serviceSelect.querySelector(
                        `option[value="${selectedServiceId}"]`
                    );

                if (serviceOption) {
                    serviceSelect.value =
                        selectedServiceId;

                    showMessage(
                        `${serviceOption.textContent} selected.`,
                        "form-message-success"
                    );
                } else {
                    showMessage(
                        "The selected service is no longer available.",
                        "form-message-warning"
                    );
                }
            }
        }

        async function loadStaff() {
            const response =
                await fetch(
                    "/api/staff/"
                );

            const data =
                await response.json();

            if (!response.ok) {
                throw new Error(
                    "Unable to load staff."
                );
            }

            staffSelect.innerHTML =
                '<option value="">Select a staff member</option>';

            const staffMembers =
                extractList(data);

            staffMembers.forEach((staff) => {
                const option =
                    document.createElement(
                        "option"
                    );

                option.value = staff.id;

                option.textContent =
                    `${staff.name} - ${staff.designation}`;

                staffSelect.appendChild(option);
            });
        }

        async function loadAvailability() {
            const staffId =
                staffSelect.value;

            const selectedDate =
                dateInput.value;

            if (!staffId || !selectedDate) {
                resetTimeSelect(
                    "Select staff and date first"
                );

                return;
            }

            resetTimeSelect(
                "Loading available times..."
            );

            const params =
                new URLSearchParams({
                    staff: staffId,
                    date: selectedDate,
                });

            try {
                const response =
                    await fetch(
                        `/api/availability/?${params.toString()}`
                    );

                const data =
                    await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.detail ||
                        "Unable to load availability."
                    );
                }

                const slots =
                    data.available_slots || [];

                timeSelect.innerHTML = "";

                if (slots.length === 0) {
                    resetTimeSelect(
                        "No times available"
                    );

                    return;
                }

                const firstOption =
                    document.createElement(
                        "option"
                    );

                firstOption.value = "";
                firstOption.textContent =
                    "Select a time";

                timeSelect.appendChild(
                    firstOption
                );

                slots.forEach((slot) => {
                    const option =
                        document.createElement(
                            "option"
                        );

                    option.value = slot;
                    option.textContent = slot;

                    timeSelect.appendChild(
                        option
                    );
                });
            } catch (error) {
                resetTimeSelect(
                    "Unable to load times"
                );

                showMessage(
                    error.message,
                    "form-message-error"
                );
            }
        }

        async function submitBooking(event) {
            event.preventDefault();

            const bookingData = {
                service: Number(
                    serviceSelect.value
                ),
                staff: Number(
                    staffSelect.value
                ),
                appointment_date:
                    dateInput.value,
                appointment_time:
                    timeSelect.value,
                notes: notesInput.value.trim(),
            };

            if (
                !bookingData.service ||
                !bookingData.staff ||
                !bookingData.appointment_date ||
                !bookingData.appointment_time
            ) {
                showMessage(
                    "Please complete all required fields.",
                    "form-message-error"
                );

                return;
            }

            submitButton.disabled = true;

            submitButton.textContent =
                "Booking...";

            showMessage(
                "Creating your appointment..."
            );

            try {
                const response =
                    await fetch(
                        "/api/appointments/",
                        {
                            method: "POST",
                            headers: authHeaders(),
                            body: JSON.stringify(
                                bookingData
                            ),
                        }
                    );

                const result =
                    await response.json();

                if (
                    response.status === 401 ||
                    response.status === 403
                ) {
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

                if (!response.ok) {
                    const errorText =
                        Object.values(result)
                            .flat()
                            .join(" ");

                    throw new Error(
                        errorText ||
                        "Unable to create appointment."
                    );
                }

                showMessage(
                    "Appointment booked successfully. Redirecting to your bookings...",
                    "form-message-success"
                );

                form.reset();

                resetTimeSelect(
                    "Select staff and date first"
                );

                window.setTimeout(() => {
                    window.location.href =
                        "/dashboard/";
                }, 1200);
            } catch (error) {
                showMessage(
                    error.message,
                    "form-message-error"
                );
            } finally {
                submitButton.disabled = false;

                submitButton.textContent =
                    "Book appointment";
            }
        }

        staffSelect.addEventListener(
            "change",
            loadAvailability
        );

        dateInput.addEventListener(
            "change",
            loadAvailability
        );

        form.addEventListener(
            "submit",
            submitBooking
        );

        const today =
            new Date()
                .toISOString()
                .split("T")[0];

        dateInput.min = today;

        Promise.all([
            loadServices(),
            loadStaff(),
        ]).catch((error) => {
            showMessage(
                error.message,
                "form-message-error"
            );
        });
    }
);