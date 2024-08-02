import frappe
from frappe.utils import today

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
