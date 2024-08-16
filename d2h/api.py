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
            item.custom_short_close_qty = item.qty - item.received_qty - item.custom_good_in_transit_qty

    purchase_order.status = "Closed"
    purchase_order.save(ignore_permissions=True)

    return "OK"

@frappe.whitelist()
def create_purchase_receipt(purchase_order, items):
    purchase_order = frappe.get_doc("Purchase Order", purchase_order)
    items_list = json.loads(items)
    
    purchase_receipt = frappe.get_doc({
        "doctype": "Purchase Receipt",
        "supplier": purchase_order.supplier,
        "currency": purchase_order.currency,
        "conversion_rate": purchase_order.conversion_rate,
        "buying_price_list": purchase_order.buying_price_list,
        "price_list_currency": purchase_order.price_list_currency,
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
        new_item.supplier_part_no = item.get("supplier_part_no")
        new_item.product_bundle = item.get("product_bundle")
        new_item.item_group = item.get("item_group")
        new_item.brand = item.get("brand")
        new_item.stock_uom = item.get("stock_uom")
        new_item.conversion_factor = item.get("conversion_factor")
        new_item.description = item.get("description")
        new_item.image = item.get("image")
        new_item.price_list_rate = item.get("price_list_rate")
        new_item.base_price_list_rate = item.get("base_price_list_rate")
        new_item.margin_type = item.get("margin_type")
        new_item.margin_rate_or_amount = item.get("margin_rate_or_amount")
        new_item.rate_with_margin = item.get("rate_with_margin")
        new_item.base_rate_with_margin = item.get("base_rate_with_margin")
        new_item.amount = item.get("amount")
        new_item.rate = item.get("rate")
        new_item.base_rate = item.get("base_rate")
        new_item.base_amount = item.get("base_amount")
        new_item.discount_percentage = item.get("discount_percentage")
        new_item.discount_amount = item.get("discount_amount")
        new_item.base_discount_amount = item.get("base_discount_amount")
        new_item.net_rate = item.get("net_rate")
        new_item.net_amount = item.get("net_amount")
        new_item.base_net_rate = item.get("base_net_rate")
        new_item.base_net_amount = item.get("base_net_amount")
        new_item.tax_rate = item.get("tax_rate")


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


@frappe.whitelist()
def short_close_sales_order(sales_order):
    sales_order = frappe.get_doc("Sales Order", sales_order)
    for item in sales_order.items:
        if item.qty > item.delivered_qty:
            item.custom_short_close_qty = item.qty - item.delivered_qty - item.custom_good_in_transit_qty

    sales_order.status = "Closed"
    sales_order.save(ignore_permissions=True)

    return "OK"

@frappe.whitelist()
def create_delivery_note(sales_order, items):
    sales_order = frappe.get_doc("Sales Order", sales_order)
    items_list = json.loads(items)
    
    delivery_note = frappe.get_doc({
        "doctype": "Delivery Note",
        "customer": sales_order.customer,
        "currency": sales_order.currency,
        "conversion_rate": sales_order.conversion_rate,
        "items": []
    })

    for item in items_list:
        new_item = delivery_note.append("items", {})
        new_item.item_code = item["item_code"]
        new_item.item_name = item["item_name"]
        new_item.qty = item["qty"]
        new_item.uom = item["uom"]
        new_item.against_sales_order = sales_order.name
        new_item.so_detail = item["name"]
        new_item.supplier_part_no = item.get("supplier_part_no")
        new_item.brand = item.get("brand")
        new_item.stock_uom = item.get("stock_uom")
        new_item.conversion_factor = item.get("conversion_factor")
        new_item.description = item.get("description")
        new_item.image = item.get("image")
        new_item.price_list_rate = item.get("price_list_rate")
        new_item.base_price_list_rate = item.get("base_price_list_rate")
        new_item.margin_type = item.get("margin_type")
        new_item.margin_rate_or_amount = item.get("margin_rate_or_amount")
        new_item.rate_with_margin = item.get("rate_with_margin")
        new_item.base_rate_with_margin = item.get("base_rate_with_margin")
        new_item.amount = item.get("amount")
        new_item.rate = item.get("rate")
        new_item.base_rate = item.get("base_rate")
        new_item.base_amount = item.get("base_amount")
        new_item.discount_percentage = item.get("discount_percentage")
        new_item.discount_amount = item.get("discount_amount")
        new_item.base_discount_amount = item.get("base_discount_amount")
        new_item.net_rate = item.get("net_rate")
        new_item.net_amount = item.get("net_amount")
        new_item.base_net_rate = item.get("base_net_rate")
        new_item.base_net_amount = item.get("base_net_amount")
        new_item.tax_rate = item.get("tax_rate")


    delivery_note.insert(ignore_permissions=True)

    for item in sales_order.items:
        found_item = next((itm for itm in items_list if itm['name'] == item.name), None)
        if found_item:
            item.custom_good_in_transit_qty += found_item['qty']

    sales_order.save(ignore_permissions=True)
    return "OK"

@frappe.whitelist()
def get_sales_order_good_in_transit(sales_order):
    delivery_notes = frappe.get_all(
        "Delivery Note Item",
        filters={
            "against_sales_order": sales_order,
            "docstatus": 1
        },
        fields=["name", "item_code", "item_name", "qty", "so_detail"]
    )
    return delivery_notes