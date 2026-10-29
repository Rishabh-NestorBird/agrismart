
# Copyright (c) 2026, rishabh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, today


class PurchaseRequest(Document):

    def validate(self):
        self.validate_requested_quantity()
        self.validate_required_by_date()
        self.validate_status_transition()

    def validate_requested_quantity(self):
        if flt(self.requested_quantity) <= 0:
            frappe.throw(_("Requested Quantity must be greater than zero."))

    def validate_required_by_date(self):
        if self.required_by_date and getdate(self.required_by_date) < getdate(today()):
            frappe.throw(_("Required By Date cannot be in the past."))

    def validate_status_transition(self):
        if self.is_new():
            return

        old_status = self.get_db_value("status")
        new_status = self.status

        if old_status == "Draft" and new_status == "Ordered":
            frappe.throw(
                _("Purchase Request must be Approved before it can be Ordered.")
            )

        if old_status == "Ordered" and new_status != "Ordered":
            frappe.throw(
                _("An Ordered Purchase Request cannot be moved to another status.")
            )
