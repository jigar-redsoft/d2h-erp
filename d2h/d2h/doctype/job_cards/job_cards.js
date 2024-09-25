// Copyright (c) 2024, ashish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Cards", {
  get_equipments: function (frm) {
    if (frm.doc.activities) {
      frappe.call({
        method: "d2h.d2h.doctype.job_cards.job_cards.get_equipments",
        args: {
          activities: frm.doc.activities.map((x) => x.activity),
        },
        callback: function (r) {
          if (r.message) {
            frm.clear_table("activity_equipments");
            r.message.forEach((element) => {
              frm.add_child("activity_equipments", {
                equipment: element.equipment,
                quantity: element.quantity,
              });
            });
            frm.refresh_field("activity_equipments");
          }
        },
      });
    }
  },
});
