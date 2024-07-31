frappe.ui.form.on("Delivery Note", {
  onload: function (frm) {
    if (
      frappe.user_roles.includes("Store Dept") &&
      !frappe.user_roles.includes("Administrator")
    ) {
      frm.set_df_property("accounting_dimensions_section", "hidden", true);
      frm.set_df_property("currency_and_price_list", "hidden", true);
      frm.set_df_property("items_section", "hidden", true);
      frm.set_df_property("section_break_30", "hidden", true);
      frm.set_df_property("section_break_49", "hidden", true);
      frm.set_df_property("taxes_section", "hidden", true);
      frm.set_df_property("section_break_46", "hidden", true);
      frm.set_df_property("totals", "hidden", true);
      frm.set_df_property("section_break_41", "hidden", true);
      frm.set_df_property("section_break_44", "hidden", true);
      frm.set_df_property("total", "hidden", true);
      frm.set_df_property("custom_section_break_jwbcu", "hidden", false);
    }
  },
});
