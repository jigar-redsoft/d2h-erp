# Copyright (c) 2024, ashish and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from datetime import datetime

class ComplaintForm(Document):
	pass


@frappe.whitelist()
def get_warranties(serial_no):
	serial_no = json.loads(serial_no)
	data = []
	for serial in serial_no:
		entry = {}
		is_serial_no_exist = frappe.db.exists("Serial No", serial["serial_no"])
		if is_serial_no_exist:
			entry["serial_no"] = serial["serial_no"]
			entry["warranty_expiry_date"] = frappe.db.get_value("Serial No", serial["serial_no"], "warranty_expiry_date")
			entry["warranty_expired"] = "False" if entry["warranty_expiry_date"] and entry["warranty_expiry_date"] > datetime.now().date()  else "True"
		else:
			entry["serial_no"] = serial["serial_no"]
			entry["warranty_expiry_date"] = None
			entry["warranty_expired"] = "True"
		data.append(entry)
	return data