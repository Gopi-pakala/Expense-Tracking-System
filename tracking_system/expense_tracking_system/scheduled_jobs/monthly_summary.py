import frappe
from frappe.utils import get_first_day, get_last_day, add_months, nowdate

def send_monthly_summary():
    # Get previous month date range
    today = nowdate()
    start_date = get_first_day(add_months(today, -1))
    end_date = get_last_day(add_months(today, -1))

    summary = frappe.db.sql("""
        SELECT
            expense_category,
            SUM(amount) AS total_amount
        FROM `tabExpense`
        WHERE posting_date BETWEEN %s AND %s
        AND workflow_state = 'Approved'
        GROUP BY expense_category
    """, (start_date, end_date), as_dict=True)
    message = f"<b>Monthly Expense Summary</b><br>"
    message += f"<b>Period:</b> {start_date} to {end_date}<br><br>"

    if not summary:
        message += "No expenses approved in this period."
    else:
        for row in summary:
            message += f"• <b>{row.expense_category}</b>: ₹{row.total_amount}<br>"

    accounts_managers = frappe.get_all(
        "Has Role",
        filters={"role": "Accounts Manager"},
        fields=["parent"]
    )

    recipients = [d.parent for d in accounts_managers]

    if not recipients:
        return

    frappe.sendmail(
        recipients=recipients,
        subject="Monthly Expense Summary Report",
        message=message
    )
