import frappe

def on_submit_purchase_receipt(doc, method):
    for item in doc.items:
        if item.purchase_order:
            item_order = frappe.get_doc("Purchase Order Item", {
                "item_code": item.item_code,
                "parent": item.purchase_order
            })
            if(item_order.custom_good_in_transit_qty > item.qty):
                item_order.custom_good_in_transit_qty -= item.qty
            else:
                item_order.custom_good_in_transit_qty = 0
            item_order.save()

def on_delete_purchase_receipt(doc, method):
    on_submit_purchase_receipt(doc, method)

def sales_order_before_load(user):
    if "Store Dept" in frappe.get_roles(user) and frappe.session.user != "Administrator":
        return """
            `tabSales Order`.name IN (
                SELECT DISTINCT sii.sales_order
                FROM `tabSales Invoice Item` sii
                JOIN `tabSales Invoice` si ON si.name = sii.parent
                WHERE si.status = 'Paid'
            )
            OR `tabSales Order`.custom_balance_status = 'Approved'
        """
    else:
        ""
