frappe.ui.form.on("Sales Order", {
  refresh: function (frm) {
    if (frm.doc.docstatus == 1 && frm.doc.status != "Closed") {
      frappe.call({
        method: "d2h.api.get_sales_order_good_in_transit",
        args: {
          sales_order: frm.doc.name,
        },
        callback: function (r) {
          pending_qty = [];
          frm.doc.items.map((item) => {
            received_qty = 0;
            r.message.map((i) => {
              if (i.so_detail == item.name) {
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
            frm.add_custom_button(__("Short Close"), function () {
              show_confirm_dialog(frm);
            });
          }
        },
      });
    }
    setTimeout(() => {
      $(`[data-label='Status'].inner-group-button`).hide();
      $(`[data-label='Status%20%3E%20Re-open'].menu-item-label`)
        .parent()
        .hide();
      $(`[data-label='Status%20%3E%20Close'].menu-item-label`).parent().hide();
      $(`[data-label='Status%20%3E%20Hold'].menu-item-label`).parent().hide();
    }, 200);
  },
  onload: function (frm) {
    setTimeout(() => {
      $(`[data-label='Status'].inner-group-button`).hide();
      $(`[data-label='Status%20%3E%20Re-open'].menu-item-label`)
        .parent()
        .hide();
      $(`[data-label='Status%20%3E%20Close'].menu-item-label`).parent().hide();
      $(`[data-label='Status%20%3E%20Hold'].menu-item-label`).parent().hide();
    }, 200);
  },
});

function show_confirm_dialog(frm) {
  frappe.confirm(
    "Are you sure? This will short close all pending items.",
    function () {
      frappe.call({
        method: "d2h.api.short_close_sales_order",
        args: {
          sales_order: frm.doc.name,
        },
        callback: function (r) {
          frappe.msgprint(
            __(`Sales Order ${frm.doc.name} has been short closed.`)
          );
          cur_frm.cscript.update_status("Close", "Closed");

          frm.refresh();
          d.hide();
        },
      });
    }
  );
}
