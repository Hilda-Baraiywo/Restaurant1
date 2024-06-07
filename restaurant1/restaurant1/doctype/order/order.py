# Copyright (c) 2024, Hilda Chepkirui and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


class Order(Document):
	pass

@frappe.whitelist(allow_guest=True)
def create_or_update_invoice(customer_id = 'Aloo-01'):
	print(f"\n\n\n success \n\n\n")
	doc = frappe.get_doc("Order", customer_id)
	customer_name = doc.customer_name

	existing_customer = frappe.get_all("Customer", filters={"customer_name": customer_name})
	if not existing_customer:
		customer = frappe.get_doc({
			'doctype': 'Customer',
			'customer_name': customer_name,
			'customer_type': "Individual",
		})
		customer.insert(ignore_permissions=True)
		frappe.db.commit()
	else:
		customer = frappe.get_doc("Customer", existing_customer[0].name)

	if doc.order_item:
		for order in doc.order_item:
			existing_item = frappe.db.get_all("Item", {"name": order.name})
			if not existing_item:
				item = frappe.get_doc({
					"doctype": "Item",
					"item_code": order.name,
					"item_name": order.name,
					"item_group": "Consumable"
				})
				item.insert(ignore_permissions=True)
				frappe.db.commit()

	existing_invoice = frappe.get_all("Sales Invoice", filters={"customer": customer.name, "status": "Draft"})
	if existing_invoice:
		invoice = frappe.get_doc("Sales Invoice", existing_invoice[0].name)
	else:
		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": customer.name,
			"items": [],
		})
		invoice.insert(ignore_permissions=True)
		frappe.db.commit()

	existing_item_codes = [item.item_code for item in invoice.get("items")]
	for order in doc.order_item:
		if order.name not in existing_item_codes:
			invoice.append("items", {
				"item_code": order.name
			})
		invoice.save(ignore_permissions=True)
		frappe.db.commit()
	return "success"

	# for order_item in order.get('items'):
	# 	menu_item = order_item.get('menu_item')
	# 	quantity = order_item.get('quantity')
	# 	price = order_item.get('price')

		# item_name = menu_item
		# existing_item = frappe.get_all("Item", {"item_name": item_name}, {'item_name', 'item_group'})
		# if not existing_item:
		# 	item = frappe.get_doc({
		# 		"doctype": "Item",
		# 		"item_code": item_name,
		# 		"item_name": item_name,
		# 		"item_group": "Menu Items",
		# 		"description": "Menu items for restaurant"
		# # 	})
		# 	item.insert()
		# 	frappe.db.commit()

		# existing_item_codes = [item.item_code for item in invoice.get("items")]

		# if item_name not in existing_item_codes:
		# 	invoice.append("items", {
		# 		"item_code": item_name,
		# 		"rate": price/quantity,
		# 		"amount": price,
		# 		"qty": quantity,
		# 	})
		# if not existing_invoice:
		# 	invoice.insert(ignore_permission=True)
		# else:
		# 	invoice.save()
		# frappe.db.commit()
