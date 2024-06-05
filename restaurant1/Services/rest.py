import frappe
from datetime import datetime, timedelta,time


@frappe.whitelist(allow_guest=True)
def save_time():
    now = datetime.now()
    today_date = now.date()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@frappe.whitelist(allow_guest=True)
def calculate_default_value():
    default_value = 0.00
    return default_value

# @frappe.whitelist(allow_guest=True)
# def validate_order():
#     if not order_data.get("customer_name"):
#         return {
#             "valid": False,
#             "error": "Customer name is required"
#         }
#     return {"valid": True}

# @frappe.whitelist(allow_guest=True)
# def calculate_total(items):
#     total = 0
#     for item in items:
#         total += item.get("quantity", 0) * item.get("price", 0)
#     return {"total": total}s