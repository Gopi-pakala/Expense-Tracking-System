# Copyright (c) 2025, Gopinadh Pakala and contributors
# For license information, please see license.txt

# import frappe



import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Category", "fieldname": "expense_category", "fieldtype": "Link", "options": "Category", "width": 150},
        {"label": "Vendor", "fieldname": "vendor", "fieldtype": "Link", "options": "Vendor", "width": 150},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Description", "fieldname": "description", "fieldtype": "Data", "width": 200},
    ]

    conditions = "1=1"

    if filters.get("from_date"):
        conditions += " AND e.posting_date >= %(from_date)s"

    if filters.get("to_date"):
        conditions += " AND e.posting_date <= %(to_date)s"

    if filters.get("employee"):
        conditions += " AND e.employee = %(employee)s"

    if filters.get("expense_category"):
        conditions += " AND e.expense_category = %(expense_category)s"

    if filters.get("vendor"):
        conditions += " AND e.vendor = %(vendor)s"

    data = frappe.db.sql(f"""
        SELECT
            e.employee,
            e.expense_category,
            e.vendor,
            e.posting_date,
            e.amount,
            e.description
        FROM
            `tabExpense` e
        WHERE
            {conditions}
        ORDER BY
            e.posting_date DESC
    """, filters, as_dict=True)

    return columns, data
