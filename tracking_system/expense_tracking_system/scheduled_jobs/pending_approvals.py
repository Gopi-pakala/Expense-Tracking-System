import frappe

def send_pending_approval_reminders():
    pending = frappe.get_all(
        "Expense",
        filters={"workflow_state": "Pending Approval"},
        fields=["name", "employee", "amount", "posting_date"]
    )

    if not pending:
        return

    message = "<b>Pending Expense Approvals</b><br><br>"
    for p in pending:
        message += f"• <b>{p.name}</b> – {p.employee}, ₹{p.amount}, {p.posting_date}<br>"

    accounts_managers = frappe.get_all(
        "Has Role",
        filters={"role": "Accounts Manager"},
        fields=["parent"]
    )

    email_list = [d.parent for d in accounts_managers]

    if not email_list:
        return

    frappe.sendmail(
        recipients=email_list,
        subject="Daily Reminder: Pending Expense Approvals",
        message=message
    )
