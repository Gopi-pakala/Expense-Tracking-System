import frappe

def notify_employee_on_approval(doc, method):
    # Only trigger when the workflow is Approved
    if doc.workflow_state != "Approved":
        return

    # Get employee email from Employee doctype
    employee_email = frappe.db.get_value("Employee", doc.employee, "company_email")

    # Fallback: send to doctype owner if employee email missing
    if not employee_email:
        employee_email = doc.owner

    # Email content
    subject = f"Your Expense {doc.name} Has Been Approved"
    message = f"""
        Hello,<br><br>
        Your expense of <b>₹{doc.amount}</b> submitted on <b>{doc.posting_date}</b> 
        has been <b style='color:green;'>Approved</b>.<br><br>
        Regards,<br>
        Finance Team
    """

    # Send email
    frappe.sendmail(
        recipients=[employee_email],
        subject=subject,
        message=message
    )
