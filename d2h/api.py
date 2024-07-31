import frappe
import json

@frappe.whitelist()
def create_stock_entry(items):
    items = json.loads(items)

    doc = frappe.new_doc("Stock Entry")
    doc.stock_entry_type = "Material Receipt"
    doc.items = []
    for item in items:
        new_item = doc.append("items", {})
        new_item.item_code = item["new_item_code"]
        new_item.qty = item["new_qty"]
        new_item.uom = item["new_uom"]
        new_item.t_warehouse = "Goods In Transit - R"

    doc.insert()
