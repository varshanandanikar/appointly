from datetime import datetime, timedelta

import frappe
from frappe import _
from frappe.utils import get_time, getdate


@frappe.whitelist(allow_guest=True)
def get_providers():
	return frappe.get_all(
		"Provider",
		filters={"is_active": 1},
		fields=["name", "provider_name", "specialization"],
		order_by="provider_name",
		ignore_permissions=True,
	)


@frappe.whitelist(allow_guest=True)
def get_available_slots(provider: str, appointment_date: str):
	provider_doc = frappe.get_doc("Provider", provider)
	if not provider_doc.is_active:
		frappe.throw(_("This provider is not currently accepting appointments."))

	duration = provider_doc.slot_duration_mins or 30
	day = getdate(appointment_date)
	start = datetime.combine(day, get_time(provider_doc.working_hours_start))
	end = datetime.combine(day, get_time(provider_doc.working_hours_end))

	booked = frappe.get_all(
		"Appointment",
		filters={
			"provider": provider,
			"appointment_date": day,
			"status": ["!=", "Cancelled"],
		},
		fields=["start_time", "end_time"],
		ignore_permissions=True,
	)
	booked_ranges = [(get_time(b.start_time), get_time(b.end_time)) for b in booked]

	slots = []
	cursor = start
	while cursor + timedelta(minutes=duration) <= end:
		slot_start = cursor.time()
		slot_end = (cursor + timedelta(minutes=duration)).time()
		overlaps = any(slot_start < b_end and slot_end > b_start for b_start, b_end in booked_ranges)
		if not overlaps:
			slots.append(cursor.strftime("%H:%M"))
		cursor += timedelta(minutes=duration)

	return slots


@frappe.whitelist(allow_guest=True)
def book_appointment(
	customer_name: str,
	phone: str,
	provider: str,
	appointment_date: str,
	start_time: str,
	email: str | None = None,
	notes: str | None = None,
):
	customer = frappe.db.get_value("Customer", {"phone": phone}, "name")
	if not customer:
		customer = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": customer_name,
			"phone": phone,
			"email": email,
		}).insert(ignore_permissions=True).name

	appointment = frappe.get_doc({
		"doctype": "Appointment",
		"customer": customer,
		"provider": provider,
		"appointment_date": appointment_date,
		"start_time": start_time,
		"notes": notes,
	})
	appointment.insert(ignore_permissions=True)
	frappe.db.commit()

	return {
		"name": appointment.name,
		"provider": appointment.provider,
		"appointment_date": str(appointment.appointment_date),
		"start_time": str(appointment.start_time),
		"end_time": str(appointment.end_time),
	}


@frappe.whitelist(allow_guest=True)
def cancel_appointment(name: str, phone: str):
	appointment = frappe.get_doc("Appointment", name)
	customer_phone = frappe.db.get_value("Customer", appointment.customer, "phone")
	if customer_phone != phone:
		frappe.throw(_("Phone number does not match this appointment."), frappe.PermissionError)

	appointment.status = "Cancelled"
	appointment.save(ignore_permissions=True)
	frappe.db.commit()
	return {"name": appointment.name, "status": appointment.status}
