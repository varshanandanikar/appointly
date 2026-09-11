### Appointly

A service appointment booking app built with [Frappe](https://frappeframework.com/) — backend doctypes/APIs plus a self-service booking portal page, all in one framework.

### Features

- **Provider**, **Customer**, and **Appointment** doctypes with proper schema (links, naming series, statuses).
- Automatic slot conflict detection — a provider can't be double-booked for an overlapping time on the same day.
- Guest-facing REST API (`appointly/api.py`): list providers, check available slots for a date, book an appointment, cancel an appointment.
- A public booking page at `/book` — pick a provider and date, see live availability, and confirm a booking, all with plain JS against the API above (no separate frontend framework needed).

### Setup

Requires a working [Frappe bench](https://github.com/frappe/frappe_docker) (Python, Node, MariaDB, Redis).

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/varshanandanikar/appointly.git
bench new-site appointly.localhost --install-app appointly
bench start
```

### Try it out

With `bench start` running, open:

```
http://appointly.localhost:8000/book
```

- Pick a provider and date, click **Check Availability**, pick a slot, fill in your name and phone, then **Confirm Booking** — you'll get a confirmation with an appointment ID (e.g. `APT-2026-00001`).
- Try booking the same slot twice — the second attempt is rejected with a conflict error.

You'll need at least one **Provider** record to book against. Log into the desk at `http://appointly.localhost:8000/app` (default: `Administrator` / the admin password you set at site creation) and add one under **Provider**, or via the console:

```bash
bench --site appointly.localhost execute frappe.client.insert --kwargs '{"doc": {"doctype": "Provider", "provider_name": "Dr. Asha Patil", "specialization": "General Consultation", "working_hours_start": "09:00:00", "working_hours_end": "13:00:00", "slot_duration_mins": 30, "is_active": 1}}'
```

Booked appointments show up under **Appointment** in the desk, same as any other Frappe record.

### API

All endpoints are whitelisted and guest-accessible, under `/api/method/appointly.api.<name>`:

| Method | Params | Description |
|---|---|---|
| `get_providers` | — | List active providers |
| `get_available_slots` | `provider`, `appointment_date` | Free time slots for that provider/date |
| `book_appointment` | `customer_name`, `phone`, `provider`, `appointment_date`, `start_time`, `email?`, `notes?` | Creates the customer (if new) and books the appointment |
| `cancel_appointment` | `name`, `phone` | Cancels a booking (phone must match the customer on record) |

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/appointly
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
