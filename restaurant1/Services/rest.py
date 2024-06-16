import json
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta,time
from frappe.utils import today

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
def update_or_create_order_item(order_id='Musila-08', order_item_name=None, menu_item='Chicken Wet Fry', quantity=1):
    print(f"Inside update_or_create_order_item with order_id: {order_id}, order_item_name: {order_item_name}, menu_item: {menu_item}, quantity: {quantity}")
    if not menu_item:
        frappe.throw("Menu Item is required", title="Missing Value")
    
    try:
        if order_item_name:
            print(f"Updating existing order item: {order_item_name}")
            order_item = frappe.get_doc("Order Item", order_item_name)
            order_item.quantity = int(quantity)  # Update quantity if order item exists
        else:
            print(f"Creating new order item for order: {order_id} with menu item: {menu_item}")
            order_item = frappe.new_doc("Order Item")
            order_item.parent = order_id
            order_item.parenttype = "Order"
            order_item.parentfield = "order_item"  # Updated parentfield to match your actual field name
            order_item.menu_item = menu_item
            order_item.quantity = int(quantity)
        
        menu_item_doc = frappe.get_doc("Menu Item", menu_item)

        if menu_item_doc:
            order_item.price = menu_item_doc.price
            order_item.total_price = menu_item_doc.price * int(quantity)
            order_item.save(ignore_permissions=True)
            print(f"Order item saved with price: {order_item.price} and total_price: {order_item.total_price}")
            
            # Recalculate total amount for the order
            total_amount = calculate_total_amount(order_id)
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
        frappe.throw(f"Order Item {order_item_name} not found", title="Not Found")


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

@frappe.whitelist(allow_guest=True)
def update_order_status(order_id='Aloo-04', status='Served'):
    order = frappe.get_doc("Order", order_id)
    if order:
        order.status = status
        order.save(ignore_permissions=True)
        frappe.msgprint(f"Order {order_id} status updated to {status}")
        return {"status": "success"}
    else:
        frappe.msgprint(f"Order {order_id} not found")
        return {"status": "error", "message": f"Order {order_id} not found"}
    
@frappe.whitelist(allow_guest=True)
def add_order_note(order_id, note):
    order = frappe.get_doc("Order", order_id)
    if order:
        order.append("order_notes", {
            "note": note,
            "added_by": frappe.session.user,
            "added_on": frappe.utils.now_datetime()
        })
        order.save(ignore_permissions=True)
        frappe.msgprint(f"Note added to Order {order_id}")
        return {"status": "success"}
    else:
        frappe.msgprint(f"Order {order_id} not found")
        return {"status": "error", "message": f"Order {order_id} not found"}
    
@frappe.whitelist(allow_guest=True)
def add_order_history(order_id='Mwangi-06', status='Pending', details=''):
    order = frappe.get_doc("Order", order_id)
    if order:
        order.append("order_history", {
            "status": status,
            "details": details,
            "changed_by": frappe.session.user,
            "changed_on": frappe.utils.now_datetime()
        })
        order.save(ignore_permissions=True)
        frappe.msgprint(f"Order history updated for Order {order_id}")
        return {"status": "success"}
    else:
        frappe.msgprint(f"Order {order_id} not found")
        return {"status": "error", "message": f"Order {order_id} not found"}
    
@frappe.whitelist(allow_guest=True)
def validate_reservation_datetime(reservation_datetime):
    today = frappe.utils.today()
    if reservation_datetime < today:
        frappe.throw("Reservation date cannot be in the past")

@frappe.whitelist(allow_guest=True)
def check_in_reservation(table_id):
    try:
        table = frappe.get_doc("Table", table_id)
        if table.status != "Reserved":
            return {'error': 'Table is not reserved'}
        reservation = frappe.get_doc("Reservation", table.current_reservation)
        reservation.status = "Checked-in"
        reservation.save(ignore_permissions=True)

        table.status = "Occupied"
        table.save(ignore_permissions=True)
        return {'success': True}
    except Exception as e:
        return {'error': str(e)}
    
@frappe.whitelist(allow_guest=True)
def confirm_reservation(reservation_id):
    try:
        reservation = frappe.get_doc("Reservation", reservation_id)
        table = frappe.get_doc("Table", reservation.table_number)

        if table.status !="Available":
            return {'error': 'Table is not available'}
        
        reservation.status = "Confirmed"
        reservation.save(ignore_permissions=True)

        table.status = "Reserved"
        table.current_reservation = reservation_id
        table.save(ignore_permissions=True)

        return {'success': True}
    except Exception as e:
        return {'error': str(e)}

@frappe.whitelist()
def mark_as_completed(reservation_id):
    try:
        reservation = frappe.get_doc("Reservation", reservation_id)
        table = frappe.get_doc("Table", reservation.table_number)
        
        reservation.status = "Completed"
        reservation.save()

        table.status = "Available"
        table.current_reservation = None
        table.save()

        return {'success': True}
    except Exception as e:
        return {'error': str(e)}

@frappe.whitelist(allow_guest=True)
def mark_as_no_show(reservation_id):
    try:
        reservation = frappe.get_doc("Reservation", reservation_id)
        table = frappe.get_doc("Table", reservation.table_number)
        
        reservation.status = "No-Show"
        reservation.save(ignore_permissions=True)

        table.status = "Available"
        table.current_reservation = None
        table.save(ignore_permissions=True)

        return {'success': True}
    except Exception as e:
        return {'error': str(e)}

@frappe.whitelist(allow_guest=True)
def cancel_reservation(reservation_id):
    try:
        reservation = frappe.get_doc("Reservation", reservation_id)
        table = frappe.get_doc("Table", reservation.table_number)
        
        reservation.status = "Cancelled"
        reservation.save(ignore_permissions=True)

        table.status = "Available"
        table.current_reservation = None
        table.save(ignore_permissions=True)

        return {'success': True}
    except Exception as e:
        return {'error': str(e)}
    
@frappe.whitelist()
def get_available_tables():
    try:
        tables = frappe.get_all("Table", filters={"status": "Available"})
        table_options = [(table.name, table.table_name) for table in tables]
        return table_options
    except Exception as e:
        frappe.throw(f"Error fetching available tables: {str(e)}")


@frappe.whitelist()
def group_tables(tables):
    try:
        tables = json.loads(tables)
        new_group = frappe.new_doc("Table Group")
        total_capacity = 0

        if not isinstance(tables, list):
            tables = [tables]

        for table_id in tables:
            table_doc = frappe.get_doc("Table", table_id)
            if table_doc.status != "Available":
                return {'error': f'Table {table_doc.table_name} is not available'}
            
            total_capacity += table_doc.capacity
            table_doc.status = "Grouped"
            table_doc.save()

            new_group.append("tables", {
                "table": table_id,
                "capacity": table_doc.capacity
            })

        new_group.total_capacity = total_capacity
        new_group.save()

        return {'success': True}
    except Exception as e:
        return {'error': str(e)}
    
@frappe.whitelist(allow_guest=True)
def add_preferences(reservation_id, preferences):
    try:
        reservation = frappe.get_doc("Reservation", reservation_id)
        reservation.preferences = preferences
        reservation.save()

        return {'success': True}
    except Exception as e:
        return {'error': str(e)}

