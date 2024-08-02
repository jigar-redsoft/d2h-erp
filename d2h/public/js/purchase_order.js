frappe.ui.form.on("Purchase Order", {
  refresh: function (frm) {
    if (!frm.is_new()) {
      qties = frm.doc.items.map((item) => {
        return item.qty - item.custom_good_in_transit_qty;
      });
      total_qty = qties.reduce((a, b) => a + b, 0);
      if (total_qty > 0) {
        frm.add_custom_button(__("Good In Transit"), function () {
          show_items_dialog(frm);
        });
      }
    }
  },
});

function show_items_dialog(frm) {
  let d = new frappe.ui.Dialog({
    title: "Items",
    fields: [
      {
        fieldname: "new_items",
        fieldtype: "Table",
        label: "Items",
        cannot_add_rows: true,
        in_place_edit: true,
        data: frm.doc.items.map((item) => {
          return {
            new_item_code: item.item_code,
            new_qty: item.qty - item.custom_good_in_transit_qty,
            new_good_in_transit_qty: 0,
          };
        }),
        fields: [
          {
            fieldtype: "Data",
            fieldname: "new_item_code",
            label: "Item Code",
            in_list_view: 1,
            columns: 4,
            read_only: 1,
          },
          {
            fieldtype: "Float",
            fieldname: "new_qty",
            label: "Pending Qty",
            in_list_view: 1,
            columns: 3,
            read_only: 1,
          },
          {
            fieldtype: "Float",
            fieldname: "new_good_in_transit_qty",
            label: "Good In Transit Qty",
            columns: 3,
            in_list_view: 1,
          },
        ],
      },
    ],
    primary_action_label: __("Save"),
    primary_action: function () {
      if (d.get_value("new_items").length) {
        d.get_value("new_items").map((item) => {
          if (item.new_good_in_transit_qty > item.new_qty) {
            frappe.throw(
              __("Good In Transit Qty cannot be greater than Pending Qty")
            );
          } else {
            frm.doc.items.map((i) => {
              if (i.item_code == item.new_item_code) {
                i.custom_good_in_transit_qty += item.new_good_in_transit_qty;
                frm.dirty();
              }
            });
            frm.refresh_field("items");
          }
        });
      }
      d.hide();
      frm.save();
    },
    secondary_action_label: __("Close"),
    secondary_action: function () {
      d.hide();
    },
  });

  d.show();
}
