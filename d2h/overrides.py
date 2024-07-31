import frappe

@frappe.whitelist()
def purchase_receipt_before_save(doc, method):
    if len(doc.items) > 0:
        doc.custom_item_duplicate = []
        for item in doc.items:
            new_item = doc.append("custom_item_duplicate", {})
            new_item.item_code = item.item_code
            new_item.qty = item.qty
            new_item.rejected_qty = item.rejected_qty

@frappe.whitelist()
def delivery_note_before_save(doc, method):
    if len(doc.items) > 0:
        doc.custom_delivery_note_item_duplicate = []
        for item in doc.items:
            new_item = doc.append("custom_delivery_note_item_duplicate", {})
            new_item.item_code = item.item_code
            new_item.qty = item.qty
            new_item.uom = item.uom