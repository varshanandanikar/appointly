# Copyright (c) 2026, Varsha Nandanikar and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Provider(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		is_active: DF.Check
		provider_name: DF.Data
		slot_duration_mins: DF.Int
		specialization: DF.Data | None
		working_hours_end: DF.Time
		working_hours_start: DF.Time
	# end: auto-generated types

	_DOCTYPE_NAME = "Provider"
