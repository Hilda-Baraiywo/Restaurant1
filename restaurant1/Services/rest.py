import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta,time

class Order(Document):
    def before_save(self):
        if not self.status:
            self.status = 'Pending'

    def after_insert(self):
        if self.status == 'Confirmed':
            frappe.publish_realtime('order_confirmed', self.name, user=self.owner)

    def on_submit(self):
        self.status = 'Completed'

@frappe.whitelist(allow_guest=True)
def save_time():
    now = datetime.now()
    today_date = now.date()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@frappe.whitelist(allow_guest=True)
def get_menu_item_price(menu_item='Pilau'):
    menu_item_doc = frappe.get_doc("Menu Item", menu_item)
    if menu_item_doc:
        return menu_item_doc.price
    else:
        return None

@frappe.whitelist(allow_guest=True)
def update_or_create_order_item(order_id='Aloo-05', order_item_name='urqd9afjgm', menu_item='Chicken Wet Fry', quantity=4):
    print(f"Inside update_or_create_order_item with order_id: {order_id}, order_item_name: {order_item_name}, menu_item: {menu_item}, quantity: {quantity}")
    if not menu_item:
        frappe.throw("Menu Item is required", title="Missing Value")
    try:
        if order_item_name:
            print(f"Updating existing order item: {order_item_name}")
            order_item = frappe.get_doc("Order Item", order_item_name)
            order_item.quantity = int(quantity)
        else:
            print(f"Creating new order item for order: {order_id} with menu item: {menu_item}")
            order_item = frappe.new_doc("Order Item")
            order_item.parent = order_id
            order_item.parenttype = "Order"
            order_item.parentfield = "items"
            order_item.menu_item = menu_item
            order_item.quantity = int(quantity)

        menu_item_doc = frappe.get_doc("Menu Item", menu_item)

        if menu_item_doc:
            order_item.price = menu_item_doc.price
            order_item.total_price = menu_item_doc.price * int(quantity)
            order_item.save(ignore_permissions=True)
            print(f"Order item saved with price: {order_item.price} and total_price: {order_item.total_price}")
            # Recalculate total amount for the order
            
            total_amount=calculate_total_amount(order_id)
            print(f"Total amount for order {order_id} recalculated: {total_amount}")
            
            return {
                'price': menu_item_doc.price,
                'total_price': order_item.total_price,
                'quantity': order_item.quantity,
                'total_amount': total_amount
            }
        else:
            print(f"Menu item {menu_item} not found")
            return {'error': 'Menu item not found'}
    except frappe.DoesNotExistError:
        print(f"Order Item {order_item_name} not found")
        frappe.throw(f"Order Item {order_item_name} not found",title="Not Found")
    

@frappe.whitelist(allow_guest=True)
def update_quantity(order_item_name='', quantity=''):
    try:
        item = frappe.get_doc("Order Item", order_item_name)
        item.quantity = int(quantity)
        item.total_price = item.price * item.quantity
        item.save(ignore_permissions=True, ignore_version=True)

        # Recalculate total amount for the order
        total_amount = calculate_total_amount(item.parent)

        return {
            'total_price': item.total_price,
            'total_amount': total_amount
        }
    except frappe.DoesNotExistError:
        frappe.throw(f"Order Item {order_item_name} not found", title="Not Found")

@frappe.whitelist(allow_guest=True)
def calculate_total_amount(order_id=''):
    order_doc = frappe.get_doc("Order", order_id)
    total_amount = sum([item.total_price for item in order_doc.order_item])
    order_doc.total_amount = total_amount
    order_doc.save(ignore_permissions=True, ignore_version=True)
    
    return total_amount
