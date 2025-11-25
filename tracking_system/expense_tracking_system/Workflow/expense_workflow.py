import frappe

def notify_employee_on_approval(doc, method):
    if doc.workflow_state != "Approved":
        return

    employee_email = frappe.db.get_value("Employee", doc.employee, "company_email")

    if not employee_email:
        employee_email = doc.owner

    subject = f"Your Expense {doc.name} Has Been Approved"
    message = f"""
        Hello,<br><br>
        Your expense of <b>₹{doc.amount}</b> submitted on <b>{doc.posting_date}</b> 
        has been <b style='color:green;'>Approved</b>.<br><br>
        Regards,<br>
        Finance Team
    """
    frappe.sendmail(
        recipients=[employee_email],
        subject=subject,
        message=message
    )
