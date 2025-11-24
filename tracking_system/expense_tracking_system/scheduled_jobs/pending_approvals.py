import frappe

def send_pending_approval_reminders():
    # Fetch pending Expense approvals
    pending = frappe.get_all(
        "Expense",
        filters={"workflow_state": "Pending Approval"},
        fields=["name", "employee", "amount", "posting_date"]
    )

    if not pending:
        return

    # Build the message body
    message = "<b>Pending Expense Approvals</b><br><br>"
    for p in pending:
        message += f"• <b>{p.name}</b> – {p.employee}, ₹{p.amount}, {p.posting_date}<br>"

    # Get all users who have the 'Accounts Manager' role
    accounts_managers = frappe.get_all(
        "Has Role",
        filters={"role": "Accounts Manager"},
        fields=["parent"]
    )

    # Extract email addresses
    email_list = [d.parent for d in accounts_managers]

    if not email_list:
        return  # No Accounts Manager found

    # Send email to all Accounts Managers
    frappe.sendmail(
        recipients=email_list,
        subject="Daily Reminder: Pending Expense Approvals",
        message=message
    )
