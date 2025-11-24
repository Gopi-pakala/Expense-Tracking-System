// Copyright (c) 2025, Gopinadh Pakala and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expense Summary"] = {
    "filters": [

        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "reqd": 1,
            "default": frappe.datetime.month_start()
        },

        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "reqd": 1,
            "default": frappe.datetime.month_end()
        },

        {
            "fieldname": "employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee",
            "reqd": 0
        },

        {
            "fieldname": "expense_category",
            "label": "Category",
            "fieldtype": "Link",
            "options": "Category",
            "reqd": 0
        },

        {
            "fieldname": "vendor",
            "label": "Vendor",
            "fieldtype": "Link",
            "options": "Vendor",
            "reqd": 0
        }
    ]
};

