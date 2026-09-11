# Copyright (c) 2026, Varsha Nandanikar and contributors
# For license information, please see license.txt

from datetime import datetime, timedelta

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_time


class Appointment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		appointment_date: DF.Date
		customer: DF.Link
		end_time: DF.Time | None
		naming_series: DF.Literal["APT-.YYYY.-"]
		notes: DF.SmallText | None
		provider: DF.Link
		start_time: DF.Time
		status: DF.Literal["Scheduled", "Completed", "Cancelled"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Appointment"

	def validate(self):
		self.set_end_time()
		self.check_for_conflicts()

	def set_end_time(self):
		slot_duration_mins = frappe.db.get_value("Provider", self.provider, "slot_duration_mins") or 30
		start = datetime.combine(datetime.today(), get_time(self.start_time))
		self.end_time = (start + timedelta(minutes=slot_duration_mins)).time()

	def check_for_conflicts(self):
		overlapping = frappe.get_all(
			"Appointment",
			filters={
				"provider": self.provider,
				"appointment_date": self.appointment_date,
				"status": ["!=", "Cancelled"],
				"name": ["!=", self.name or ""],
				"start_time": ["<", self.end_time],
				"end_time": [">", self.start_time],
			},
			pluck="name",
			ignore_permissions=True,
		)
		if overlapping:
			frappe.throw(
				_("{0} already has an appointment ({1}) that overlaps this time slot.").format(
					self.provider, overlapping[0]
				)
			)
