// Copyright (c) 2025, Gopinadh Pakala and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vendor Payments"] = {
    "filters": [
        {
            "fieldname": "vendor",
            "label": "Vendor",
            "fieldtype": "Link",
            "options": "Vendor"
        },
        {
            "fieldname": "vendor_type",
            "label": "Vendor Type",
            "fieldtype": "Select",
            "options": "Please Select\nService\nBill\nProduct\nOthers"
        }
    ]
};
