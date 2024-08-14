import frappe
from frappe.utils import today
import json

LIMIT_PER_DAY = 2

@frappe.whitelist()
def increment_print_count():
    current_date = today()

    print_log = frappe.cache().hget('global_daily_print_log', 'count') or {}

    if print_log.get('date') != current_date:
        print_log = {'count': 0, 'date': current_date}

    if print_log['count'] > LIMIT_PER_DAY:
        return {'limit_reached': True}

    print_log['count'] += 1
    frappe.cache().hset('global_daily_print_log', 'count', print_log)

    return {'limit_reached': False}

def before_print(_, __, ___):
    current_date = today()

    print_log = frappe.cache().hget('global_daily_print_log', 'count')

    if not print_log:
        return

    if print_log.get('date') != current_date:
        return

    if print_log['count'] > LIMIT_PER_DAY:
        frappe.throw('The daily print limit for all documents has been reached.')


@frappe.whitelist()
def short_close_purchase_order(purchase_order):
    purchase_order = frappe.get_doc("Purchase Order", purchase_order)
    for item in purchase_order.items:
        if item.qty > item.received_qty:
            item.custom_short_close_qty = item.qty - item.received_qty

    purchase_order.save(ignore_permissions=True)
    frappe.msgprint(f"Purchase Order {purchase_order.name} has been short closed.")


@frappe.whitelist()
def create_purchase_receipt(purchase_order, items):
    purchase_order = frappe.get_doc("Purchase Order", purchase_order)
    items_list = json.loads(items)
    
    purchase_receipt = frappe.get_doc({
        "doctype": "Purchase Receipt",
        "supplier": purchase_order.supplier,
        "items": []
    })

    for item in items_list:
        new_item = purchase_receipt.append("items", {})
        new_item.item_code = item["item_code"]
        new_item.item_name = item["item_name"]
        new_item.qty = item["qty"]
        new_item.uom = item["uom"]
        new_item.purchase_order = purchase_order.name
        new_item.purchase_order_item = item["name"]
        new_item.scheduled_date = purchase_order.schedule_date


    purchase_receipt.insert(ignore_permissions=True)

    for item in purchase_order.items:
        found_item = next((itm for itm in items_list if itm['name'] == item.name), None)
        if found_item:
            item.custom_good_in_transit_qty += found_item['qty']

    purchase_order.save(ignore_permissions=True)
    return "OK"

@frappe.whitelist()
def get_purchase_order_good_in_transit(purchase_order):
    purchase_receipts = frappe.get_all(
        "Purchase Receipt Item",
        filters={
            "purchase_order": purchase_order,
            "docstatus": 1
        },
        fields=["name", "item_code", "item_name", "qty", "purchase_order_item"]
    )
    return purchase_receipts