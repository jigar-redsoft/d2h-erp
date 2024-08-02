$(document).ready(function () {
  setTimeout(() => {
    $(`button[data-label='Print']`).on("click", function (e) {
      frappe.call({
        method: "d2h.api.increment_print_count",
        callback: function (r) {
          if (r.message && r.message.limit_reached) {
            frappe.throw(
              "The daily print limit for all documents has been reached."
            );
          } else {
            frm.print_doc();
          }
        },
      });
    });
  }, 500);
});
