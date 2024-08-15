// Copyright (c) 2024, ashish and contributors
// For license information, please see license.txt

frappe.query_reports["Short Close Order Report"] = {
  filters: [
    {
      fieldname: "company",
      label: __("Company"),
      fieldtype: "Link",
      width: "80",
      options: "Company",
      reqd: 1,
      default: frappe.defaults.get_default("company"),
    },
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
      width: "80",
      reqd: 1,
      default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
      width: "80",
      reqd: 1,
      default: frappe.datetime.get_today(),
    },
    {
      fieldname: "name",
      label: __("Purchase Order"),
      fieldtype: "Link",
      width: "80",
      options: "Purchase Order",
      get_query: () => {
        return {
          filters: { docstatus: 1 },
        };
      },
    },
  ],
};
