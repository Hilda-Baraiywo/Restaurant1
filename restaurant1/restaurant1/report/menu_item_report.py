import frappe
from restaurant1.utils import restaurant1

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_data(filters):
    conditions = "1=1"
    if filters.get("start_date"):
        conditions += f" AND `tabOrder`.`transaction_date` >= '{filters.get('start_date')}'"
    if filters.get("end_date"):
        conditions += f" AND `tabOrder`.`transaction_date` <= '{filters.get('end_date')}'"
    if filters.get("menu_item"):
        conditions += f" AND `tabOrder Item`.`menu_item` = '{filters.get('menu_item')}'"

    SQL = f"""
        SELECT 
            `tabOrder Item`.`menu_item`, 
            SUM(`tabOrder Item`.`quantity`) AS `total_quantity_sold`,
            SUM(`tabOrder Item`.`price` * `tabOrder Item`.`quantity`) AS `total_sales_amount`
        FROM 
            `tabOrder Item`
        JOIN
            `tabOrder` ON `tabOrder Item`.`parent` = `tabOrder`.`name`
        WHERE
            {conditions}
        GROUP BY 
            `tabOrder Item`.`menu_item`
        ORDER BY 
            `total_sales_amount` DESC
    """
    data = frappe.db.sql(SQL, as_dict=True)
    return data

def get_columns():
    return [
        {"fieldname": "menu_item", "label": "Menu Item", "fieldtype": "Link", "options": "Menu Item", "width": 200},
        {"fieldname": "total_quantity_sold", "label": "Total Quantity Sold", "fieldtype": "Float", "width": 200},
        {"fieldname": "total_sales_amount", "label": "Total Sales Amount", "fieldtype": "Currency", "width": 200}
    ]