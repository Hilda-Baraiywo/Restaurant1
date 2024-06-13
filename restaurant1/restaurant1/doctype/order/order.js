// Copyright (c) 2024, Hilda Chepkirui and contributors
// For license information, please see license.txt

frappe.ui.form.on("Order", {
    onload: function(frm) {
        if (!frm.doc.status) {
            frm.set_value('status', 'Pending');
        }
    },

    refresh: function(frm){
        frm.add_custom_button(__('Create/Update Invoice'), function(){
            frappe.call({
                method: 'restaurant1.restaurant1.doctype.order.order.create_or_update_invoice',
                args: {
                    order_id: frm.doc.name
                },
                callback: function(response) {
                    if (response.message === 'success') {
                        frappe.msgprint('Invoice created/updated successfully.');
                        frm.reload_doc();
                    } else {
                        frappe.msgprint('Failed to create/update invoice: ' + response.message.error);
                    }
                } 
            });
        }).addClass('btn-primary')
    },

    validate: function(frm) {
        // Update item information based on order items
        frm.doc.order_item.forEach(function(item) {
            frappe.call({
                method: 'restaurant1.restaurant1.doctype.order.order.update_or_create_item',
                args: {
                    order_id: frm.doc.name,
                    item_name: item.menu_item,
                    price: item.price,
                    quantity: item.quantity
                },
                callback: function(response) {
                    if (response.message === 'success') {
                        frappe.msgprint('Item updated/created successfully.');
                        frm.reload_doc();
                    } else {
                        frappe.msgprint('Failed to update/create item: ' + response.message.error);
                    }
                }
            });
        });
    },

    validate: function(frm) {
        frappe.call({
            method: 'restaurant1.Services.rest.save_time',
            callback: function(r) {
                if (r.message) {
                    frm.set_value('order_datetime', r.message);
                }
            }
        });
    },   

});

frappe.ui.form.on('Order Item', {

    menu_item: function(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        // let menu_item = item.menu_item || '';

        // if (menu_item && menu_item !== 'None') {
        frappe.call({
            method: 'restaurant1.Services.rest.update_or_create_order_item',
            args: {
                'order_id': frm.doc.name,
                'order_item_name': item.name,
                'menu_item': menu_item,
                'quantity': item.quantity || 0
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, 'price', r.message.price);
                    frappe.model.set_value(cdt, cdn, 'total_price', r.message.total_price);
                    frappe.model.set_value(cdt, cdn, 'quantity', r.message.quantity);
                    frm.set_value('total_amount', r.message.total_amount);
                }
            }
        });
    },

    quantity: function(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        frappe.call({
            method: 'restaurant1.Services.rest.update_quantity',
            args: {
                'order_item_name': item.name,
                'quantity': item.quantity
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, 'total_price', r.message.total_price);
                    frm.set_value('total_amount', r.message.total_amount);
                }
            }
        });
    }

});
function update_total_amount(frm) {
    frappe.call({
        method: 'restaurant1.Services.rest.calculate_total_amount',
        args: {
            'order_id': frm.doc.name
        },
        callback: function(r) {
            if (r.message) {
                frm.set_value('total_amount', r.message);
                frm.refresh_field('total_amount');
            } else {
                frappe.msgprint('Failed to update total amount');
            }
        }
    });
}

