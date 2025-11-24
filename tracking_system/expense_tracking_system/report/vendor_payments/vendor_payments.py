# Copyright (c) 2025, Gopinadh Pakala and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Vendor Name", "fieldname": "vendor_name", "fieldtype": "Data", "width": 180},
        {"label": "Vendor Type", "fieldname": "vendor_type", "fieldtype": "Data", "width": 140},
        {"label": "GST Number", "fieldname": "gst_number", "fieldtype": "Data", "width": 140},
        {"label": "Mode of Payment", "fieldname": "mode_of_payment", "fieldtype": "Link", "options": "Mode of Payment", "width": 150},
        {"label": "Email", "fieldname": "email", "fieldtype": "Data", "width": 180},
        {"label": "Total Amount Paid", "fieldname": "total_amount_paid", "fieldtype": "Currency", "width": 160},
        {"label": "Contact Number", "fieldname": "contact", "fieldtype": "Data", "width": 150},
        {"label": "Address", "fieldname": "address", "fieldtype": "Data", "width": 200},
    ]

    conditions = "1=1"

    if filters.get("vendor"):
        conditions += " AND v.name = %(vendor)s"

    if filters.get("vendor_type"):
        conditions += " AND v.vendor_type = %(vendor_type)s"

    data = frappe.db.sql(f"""
        SELECT
            v.vendor_name,
            v.vendor_type,
            v.gst_number,
            v.mode_of_payment,
            v.email,
            v.total_amount_paid,
            v.contact,
            v.address
        FROM
            `tabVendor` v
        WHERE
            {conditions}
        ORDER BY
            v.vendor_name ASC
    """, filters, as_dict=True)

    return columns, data
