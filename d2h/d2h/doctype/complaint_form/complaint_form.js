// Copyright (c) 2024, ashish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Complaint Form", {
  warranty_expiry_date: function (frm) {
    const today = frappe.datetime.nowdate();
    if (today > frm.doc.warranty_expiry_date) {
      frappe.msgprint("The warranty period has expired.");
      frm.set_value("warranty_status", "True");
    }
  },
});
