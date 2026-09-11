# Copyright (c) 2026, Varsha Nandanikar and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _
from frappe.model.document import Document

PHONE_RE = re.compile(r"^[6-9]\d{9}$")


class Customer(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		customer_name: DF.Data
		email: DF.Data | None
		phone: DF.Data
	# end: auto-generated types

	_DOCTYPE_NAME = "Customer"

	def validate(self):
		self.validate_phone()

	def validate_phone(self):
		phone = (self.phone or "").strip()
		if not PHONE_RE.match(phone):
			frappe.throw(_("Enter a valid 10-digit phone number."))
		self.phone = phone
