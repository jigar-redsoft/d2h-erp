// Copyright (c) 2024, ashish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Cards", {
  get_items: function (frm) {
    if (frm.doc.activities) {
      frappe.call({
        method: "d2h.d2h.doctype.job_cards.job_cards.get_items",
        args: {
          activities: frm.doc.activities.map((x) => x.activity),
        },
        callback: function (r) {
          if (r.message) {
            frm.clear_table("activity_items");
            r.message.forEach((element) => {
              frm.add_child("activity_items", {
                item: element.item,
                quantity: element.quantity,
              });
            });
            frm.refresh_field("activity_items");
          }
        },
      });
    }
  },
});
