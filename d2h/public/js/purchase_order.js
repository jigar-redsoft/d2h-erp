frappe.ui.form.on("Purchase Order", {
  refresh: function (frm) {
    if (!frm.is_new()) {
      frm.add_custom_button(__("Good In Transit"), function () {
        show_items_dialog(frm);
      });
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
        get_data: () => {
          data = [];
          frm.doc.items.forEach((item) => {
            data.push({
              new_item_code: item.item_code,
              new_uom: item.uom,
              new_qty: item.qty,
            });
          });
          return data;
        },
        fields: [
          {
            fieldtype: "Data",
            fieldname: "new_item_code",
            label: "Item Code",
            in_list_view: 1,
            read_only: 1,
          },
          {
            fieldtype: "Data",
            fieldname: "new_uom",
            label: "UOM",
            in_list_view: 1,
            read_only: 1,
          },
          {
            fieldtype: "Float",
            fieldname: "new_qty",
            label: "Quantity",
            in_list_view: 1,
          },
        ],
      },
    ],
    primary_action_label: __("Create"),
    primary_action: function () {
      frappe.call({
        method: "d2h.api.create_stock_entry",
        args: {
          items: JSON.stringify(d.get_values().new_items),
        },
        callback: function (r) {
          if (!r.exc) {
            frappe.msgprint(__("Stock Entry Created"));
            d.hide();
          }
        },
      });
    },
    secondary_action_label: __("Close"),
    secondary_action: function () {
      d.hide();
    },
  });

  d.show();
}
