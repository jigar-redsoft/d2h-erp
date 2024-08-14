frappe.ui.form.on("Purchase Order", {
  refresh: function (frm) {
    if (frm.doc.docstatus == 1) {
      frappe.call({
        method: "d2h.api.get_purchase_order_good_in_transit",
        args: {
          purchase_order: frm.doc.name,
        },
        callback: function (r) {
          pending_qty = [];
          frm.doc.items.map((item) => {
            received_qty = 0;
            r.message.map((i) => {
              if (i.purchase_order_item == item.name) {
                received_qty += i.qty;
              }
            });
            if (received_qty < item.qty) {
              pending_qty.push({
                name: item.name,
                pending: item.qty - received_qty,
              });
            }
          });
          if (pending_qty.length > 0) {
            frm.add_custom_button(__("Good In Transit"), function () {
              show_items_dialog(frm, pending_qty);
            });
            frm.add_custom_button(__("Short Close"), function () {
              show_confirm_dialog(frm);
            });
          }
        },
      });
    }
  },
});

function show_items_dialog(frm, pending_qty) {
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
            name: item.name,
            new_item_code: item.item_code,
            new_qty: pending_qty.find((i) => i.name == item.name)
              ? pending_qty.find((i) => i.name == item.name).pending -
                item.custom_good_in_transit_qty
              : qty,
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
            items_for_purchase_receipt = [];

            frm.doc.items.map((i) => {
              if (i.name == item.name && item.new_good_in_transit_qty) {
                items_for_purchase_receipt.push({
                  name: i.name,
                  item_code: i.item_code,
                  item_name: i.item_name,
                  qty: item.new_good_in_transit_qty,
                  uom: i.uom,
                });
              }
            });

            if (items_for_purchase_receipt.length > 0) {
              frappe.call({
                method: "d2h.api.create_purchase_receipt",
                args: {
                  purchase_order: frm.doc.name,
                  items: JSON.stringify(items_for_purchase_receipt),
                },
                callback: function () {
                  frm.dirty();
                  frappe.msgprint(__("Purchase Receipt has been created."));
                  frm.refresh_field("items");
                  d.hide();
                },
              });
            }
          }
        });
      }
    },
    secondary_action_label: __("Close"),
    secondary_action: function () {
      d.hide();
    },
  });

  d.show();
}

function show_confirm_dialog(frm) {
  frappe.confirm(
    "Are you sure? This will short close all pending items.",
    function () {
      frappe.call({
        method: "d2h.api.short_close_purchase_order",
        args: {
          purchase_order: frm.doc.name,
        },
        callback: function (r) {
          frappe.msgprint(__("Items have been short closed."));
          frm.refresh();
          d.hide();
        },
      });
    }
  );
}
