
# Copyright (c) 2026, rishabh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class StockTransaction(Document):

    def validate(self):
        if flt(self.quantity) <= 0:
            frappe.throw(_("Quantity must be greater than zero."))

        if self.transaction_type not in ("Stock In", "Stock Out"):
            frappe.throw(
                _("Transaction Type must be Stock In or Stock Out.")
            )

        # Stock Out ke liye available stock check karo.
        # Existing submitted transaction ko edit karne ka option nahi hai.
        if self.transaction_type == "Stock Out" and self.docstatus == 0:
            item = frappe.get_doc(
                "Inventory Item", self.inventory_item
            )

            if flt(item.current_stock) < flt(self.quantity):
                frappe.throw(
                    _("Insufficient stock. Available: {0}, Required: {1}").format(
                        item.current_stock,
                        self.quantity,
                    )
                )

    def on_submit(self):
        self.recalculate_stock()

    def on_cancel(self):
        self.recalculate_stock()

    def recalculate_stock(self):
        if not self.inventory_item:
            frappe.throw(_("Please select an Inventory Item."))

        item = frappe.get_doc(
            "Inventory Item", self.inventory_item
        )

        # Sirf submitted transactions calculate hongi.
        # Current document ko alag se add/subtract nahi karna.
        result = frappe.db.sql(
            """
            SELECT COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Stock In'
                            THEN quantity
                        WHEN transaction_type = 'Stock Out'
                            THEN -quantity
                        ELSE 0
                    END
                ),
                0
            ) AS calculated_stock
            FROM `tabStock Transaction`
            WHERE inventory_item = %s
              AND docstatus = 1
            """,
            (self.inventory_item,),
            as_dict=True,
        )

        calculated_stock = flt(result[0].calculated_stock)

        if calculated_stock < 0:
            frappe.throw(
                _("Stock cannot be negative. Calculated stock: {0}").format(
                    calculated_stock
                )
            )

        item.current_stock = calculated_stock
        item.save()

        # Low-stock alert
        if calculated_stock <= flt(item.reorder_level):
            frappe.msgprint(
                _(
                    "Low Stock Alert! Item: {0}, Current Stock: {1}, "
                    "Reorder Level: {2}"
                ).format(
                    item.item_name,
                    calculated_stock,
                    item.reorder_level,
                ),
                title=_("Low Stock Alert"),
                indicator="orange",
            )
