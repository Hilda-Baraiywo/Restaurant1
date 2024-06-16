// Copyright (c) 2024, Hilda Chepkirui and contributors
// For license information, please see license.txt

frappe.ui.form.on("Order", {
    onload: function(frm) {
        if (!frm.doc.status) {
            frm.set_value('status', 'Pending');
        }
    },

    refresh: function(frm){
        loadOrderHistory(frm);

        if (frm.doc.status === 'Pending'){
            frm.add_custom_button(__('Confirm Order'), function(){
                updateOrderStatus(frm.doc.name, 'Confirmed');
            }).addClass('btn-primary');
        }

        if (frm.doc.status === 'Confirmed' || frm.doc.status === 'Preparing') {
            frm.add_custom_button(__('Cancel Order'), function() {
                updateOrderStatus(frm.doc.name, 'Cancelled');
            }).addClass('btn-danger');
        }

        if (frm.doc.status == 'Confirmed') {
            frm.add_custom_button(__('Start Preparation'), function(){
                updateOrderStatus(frm.doc.name, 'Preparing');
            }).addClass('btn-primary');
        }

        if (frm.doc.status === 'Preparing') {
            frm.add_custom_button(__('Order Ready'), function(){
                updateOrderStatus(frm.doc.name, 'Served');
            }).addClass('btn-success');
        }
        frm.add_custom_button(__('Create/Update Invoice'), function(){
            frappe.confirm(
                'Are you sure you want to create or update the invoice?',
                function(){
                    frappe.call({
                        method: 'restaurant1.restaurant1.doctype.order.order.create_or_update_invoice',
                        args:{
                            order_id: frm.doc.name,
                            confirmed: true
                        },
                        callback: function(response) {
                            if (response.message && response.message.success) {
                                frappe.msgprint('Invoice created/updated successfully.');
                                frm.reload_doc();
                            }else if (response.message && response.message.error) {
                                frappe.msgprint('Failed to create/update invoice: '+ response.message.error);
                            }else if (response.message && response.message.confrim){
                                frappe.msgprint('Invoice creation/update cancelled.');
                            }
                        }
                    });
                },
                function(){
                    frappe.msgprint('Invoice creation/update cancelled.');
                }
            );
        }).addClass('btn-primary');

        frm.add_custom_button(__('Add Menu Item'), function(){
            frappe.prompt({
                fieldname: 'menu_item',
                fieldtype: 'Link',
                options: 'Menu Item',
                label: 'Menu Item',
                reqd: 1,
                get_query: function(){
                    return {
                        filters: {
                            'is_available': 1
                        }
                    };
                }
            }, function(values){
                frappe.call({
                    method: 'restaurant1.Services.rest.get_menu_item_price',
                    args: {
                        'menu_item': values.menu_item
                    },
                    callback: function(r){ 
                        if (r.message){
                            var existing_item =frm.doc.order_item.find(item => item.menu_item === values.menu_item);
                            if (existing_item){
                                frappe.model.set_value(existing_item.doctype, existing_item.name, 'quantity', existing_item.quantity + 1);
                                frappe.model.set_value(existing_item.doctype, existing_item.name, 'total_price', r.message * existing_item.quantity);
                            } else {
                                var child = frm.add_child('order_item');
                                frappe.model.set_value(child.doctype, child.name, 'menu_item', values.menu_item);
                                frappe.model.set_value(child.doctype, child.name, 'price', r.message);
                                frappe.model.set_value(child.doctype, child.name, 'quantity', 1);
                                frappe.model.set_value(child.doctype, child.name, 'total_price', r.message);
                            }
                            frm.refresh_field('order_item');
                        }
                    }
                });
            }, __('Select Menu Item'), __('Add'));
        }).addClass('btn-primary');

        frm.add_custom_button(__('Add Order Note'), function(){
            frappe.prompt({
                label: 'Note',
                fieldname: 'note',
                fieldtype: 'Text',
                reqd: true
            }, function(values) {
                addOrderNote(frm.doc.name, values.note);
            }, 'Add Note', 'Add');
        }).addClass('btn-primary');
    },

    validate: function(frm) {
        // Update item information based on order items
        frm.doc.order_item.forEach(function(item) {
            frappe.call({
                method: 'restaurant1.restaurant1.doctype.order.order.update_or_create_order_item',
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

    onload_post_render: function(frm) {
        frappe.call({
            method: 'restaurant1.Services.rest.save_time',
            callback: function(r) {
                if (r.message) {
                    frm.set_value('order_datetime', r.message);
                }
            }
        });
        loadOrderHistory(frm);
    },   

});

function updateOrderStatus(order_id, status){
    frappe.call({
        method: 'restaurant1.Services.rest.update_order_status',
        args: {
            order_id: order_id,
            status: status
        },
        callback: function(response){
            if (response.message && response.message.status === 'success'){
                cur_frm.reload_doc();
            } else {
                frappe.msgprint(`Failed to update order staus: ${response.message}`);
            }
        }
    });
}

function addOrderNote(order_id, note){
    frappe.call({
        method: 'restaurant1.Services.rest.add_order_note',
        args: {
            order_id: order_id,
            note: note
        },
        callback: function(response) {
            if  (response.message && response.message.status === 'success') {
                frappe.msgprint(`Note added to the Order ${order_id}`);
                cur_frm.reload_doc();
            } else {
                frappe.msgprint('Failed to add note: ${response.message}');
            }
        }
    });
}

function loadOrderHistory(frm) {
    if (frm.doc.__islocal) return;
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Order History',
            filters: { 'parent': frm.doc.name },
            fields: ['sataus', 'details', 'changed_by', 'changed_on'],
            order_by: 'changed_on desc'
        },
        callback: function(message) {
            if (response.message) {
                var order_history = response.message;
                var history_html = '<ul>';
                order_history.forEach(function(hist) {
                    history_html += `<li><b>${hist.status}</b>: ${hist.details} (by ${hist.changed_by} on ${hist.changed})</li>`;
                });
                history_html += '</ul>';
                frm.dashboard.add_indicator('Order History', history_html, 'orange');
            }
        }
    });
}

frappe.ui.form.on('Order Item', {
    menu_item: function(frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        frappe.call({
            method: 'restaurant1.Services.rest.get_menu_item_price',
            args: {
                'menu_item': item.menu_item
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, 'price', r.message);
                    frappe.model.set_value(cdt, cdn, 'total_price', flt(r.message) * flt(item.quantity));
                    update_total_amount(frm);
                    frm.refresh_field('order_item');
                }
            }
        });
    },

    quantity: function(frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'total_price', flt(item.price) * flt(item.quantity));
        update_total_amount(frm);
        frm.refresh_field('order_item');
    }
});

function update_total_amount(frm) {
    var total_amount = 0;
    frm.doc.order_item.forEach(function(item) {
        total_amount += flt(item.total_price);
    });
    frm.set_value('total_amount', total_amount);
    frm.refresh_field('total_amount');
}


