# Copyright (c) 2024, ashish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class JobCards(Document):
	pass

@frappe.whitelist()
def get_items(activities):
	activities = json.loads(activities)
	data = []
	for activity in activities:
		items = frappe.get_all("Activity Item", filters={"parent": activity}, fields=["item", "quantity"])
		for item in items:
			data.append({
				"item": item.item,
				"quantity": item.quantity
			})
	return data