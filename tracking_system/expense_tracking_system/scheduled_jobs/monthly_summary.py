import frappe
from frappe.utils import get_url, today, formatdate
from frappe.utils import get_url, formatdate, nowdate
from frappe.utils.data import add_months, get_first_day, get_last_day

def send_monthly_expense_summary():
    """Sends a monthly summary report of expenses grouped by category."""
 
    today = nowdate()
    first_day = get_first_day(today)
    last_day = get_last_day(today)
 
    # Get monthly expense totals grouped by category
    monthly_data = frappe.db.sql(
        """
        SELECT
            expense_category,
            SUM(amount) AS total_amount
        FROM `tabExpense`
        WHERE posting_date BETWEEN %s AND %s
        GROUP BY expense_category
        ORDER BY total_amount DESC
        """,
        (first_day, last_day),
        as_dict=True,
    )
 
    if not monthly_data:
        frappe.logger().info("No monthly summary data available.")
        return
 
    # Fetch Accounts Manager users WITH valid email
    accounts_managers = frappe.db.sql(
        """
        SELECT DISTINCT u.email
        FROM `tabUser` u
        JOIN `tabHas Role` hr ON hr.parent = u.name
        WHERE hr.role = 'Account Manager'
          AND u.enabled = 1
          AND IFNULL(u.email, '') != ''
        """,
        as_dict=True,
    )
 
    if not accounts_managers:
        frappe.logger().warning("No Accounts Manager users found for monthly summary.")
        return
 
    recipients = [u["email"] for u in accounts_managers]
 
    # Build rows for email table
    rows = ""
    total_month_amount = 0
 
    for row in monthly_data:
        category = row.expense_category or "Uncategorized"
        amount = row.total_amount or 0
 
        rows += f"""
            <tr>
                <td>{category}</td>
                <td>{frappe.format_value(amount, "Currency")}</td>
            </tr>
        """
 
        total_month_amount += amount
 
    # Email subject & content
    subject = f"Monthly Expense Summary — {formatdate(today, 'MMMM yyyy')}"
 
    message = f"""
        <p>Hello,</p>
        <p>Here is the monthly expense summary for
        <b>{formatdate(today, 'MMMM yyyy')}</b>:</p>
 
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
            <tr>
                <th>Expense Category</th>
                <th>Total Amount</th>
            </tr>
            {rows}
            <tr style="font-weight: bold; background-color: #f1f1f1;">
                <td>Total</td>
                <td>{frappe.format_value(total_month_amount, "Currency")}</td>
            </tr>
        </table>
 
        <p>Date: {formatdate(today)}</p>
        <p>This is an automated monthly summary from ERPNext.</p>
    """
 
    # Send the email automatically
    try:
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message
               # <-- IMPORTANT (Auto send immediately)
        )
 
        # Also process any queued emails (failsafe)
        frappe.enqueue("frappe.email.doctype.email_queue.email_queue.send_regular")
 
        frappe.logger().info(
            "Monthly summary email sent automatically to: " + ", ".join(recipients)
        )
 
    except Exception:
        frappe.log_error("Error while sending monthly summary email")
        raise