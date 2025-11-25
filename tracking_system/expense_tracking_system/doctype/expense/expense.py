# Copyright (c) 2025, Gopinadh Pakala and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, date_diff
 
class Expense(Document):
 
    def on_update(self):
        """Check if expense is overdue and escalate."""
        self.check_overdue_and_escalate()
 
    def check_overdue_and_escalate(self):
        if self.workflow_state != "Pending Approval":
            return
 
        if not self.posting_date:
            return
 
        days_pending = date_diff(nowdate(), self.posting_date)
 
        if days_pending > 7:
            frappe.db.set_value("Expense", self.name, "workflow_state", "Escalated")
 
            frappe.get_doc({
                "doctype": "Comment",
                "comment_type": "Info",
                "reference_doctype": "Expense",
                "reference_name": self.name,
                "content": f"Auto-escalated after {days_pending} days of Pending Approval."
            }).insert(ignore_permissions=True)