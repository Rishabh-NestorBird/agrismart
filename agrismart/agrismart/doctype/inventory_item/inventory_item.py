
# Copyright (c) 2026, rishabh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class InventoryItem(Document):

    def validate(self):
        if flt(self.current_stock) < 0:
            frappe.throw(_("Current Stock cannot be negative."))

        if flt(self.reorder_level) <= 0:
            frappe.throw(_("Reorder Level must be greater than zero."))

    # def on_update(self):
    #     if flt(self.current_stock) <= flt(self.reorder_level):
    #         frappe.msgprint(
    #             _("Low Stock Alert! Current Stock is {0}, Reorder Level is {1}.")
    #             .format(self.current_stock, self.reorder_level),
    #             title=_("Low Stock Alert"),
    #             indicator="orange"
    #         )
