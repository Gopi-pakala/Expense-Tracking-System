// Copyright (c) 2025, Gopinadh Pakala and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense', {
    amount(frm) {
        if (!frm.doc.expense_category || !frm.doc.amount) {
            return;
        }
 
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Category",
                fieldname: "limit_per_transaction",
                filters: { name: frm.doc.expense_category }
            },
            callback(r) {
                if (r && r.message) {
                    let limit = r.message.limit_per_transaction;
 
                    if (frm.doc.amount > limit) {
                        frappe.msgprint({
                            title: "Limit Exceeded",
                            message: `Amount exceeds the allowed limit for this category.<br><br>
<b>Category Limit:</b> ${limit}<br>
<b>Entered Amount:</b> ${frm.doc.amount}`,
                            indicator: "red"
                        });
 
                        frm.set_value("amount", "");
                    }
                }
            }
        });
    }
});