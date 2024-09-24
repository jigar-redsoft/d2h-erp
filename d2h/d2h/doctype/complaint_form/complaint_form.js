// Copyright (c) 2024, ashish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Complaint Form", {
  get_warranties: function (frm) {
    if (frm.doc.serial_no) {
      frappe.call({
        method: "d2h.d2h.doctype.complaint_form.complaint_form.get_warranties",
        args: {
          serial_no: frm.doc.serial_no,
        },
        callback: function (r) {
          if (r.message) {
            frm.clear_table("serial_no");
            r.message.forEach((element) => {
              frm.add_child("serial_no", {
                serial_no: element.serial_no,
                warranty_expiry_date: element.warranty_expiry_date,
                warranty_expired: element.warranty_expired,
              });
            });
            frm.refresh_field("serial_no");
          }
        },
      });
    } else {
      frappe.msgprint("Please Enter Serial Number");
    }
  },
});
