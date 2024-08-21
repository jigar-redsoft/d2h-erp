$(document).on("page-change", function () {
  if (document.baseURI.includes("/app/print/")) {
    $(`button[data-label='Print']`).hide();
    frappe.call({
      method: "d2h.api.get_print_limit",
      callback: function (r) {
        if (r.message && !r.message.limit_reached) {
          $(`button[data-label='Print']`).show();
          $(`button[data-label='Print']`).on("click", function (e) {
            frappe.call({
              method: "d2h.api.increment_print_count",
              callback: function (r) {
                if (r.message && r.message.limit_reached) {
                  frappe.throw(
                    "The daily print limit for all documents has been reached."
                  );
                }
              },
            });
          });
        }
      },
    });
  }
});
