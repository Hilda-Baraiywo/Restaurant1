// Copyright (c) 2024, Hilda Chepkirui and contributors
// For license information, please see license.txt

frappe.ui.form.on("Reservation", {
    validate: function(frm) {
        var today = new Date();
        var reservation_datetime = new Date(frm.doc.reservation_datetime);
        
        if (reservation_datetime < today) {
            frappe.msgprint(__("Reservation date cannot be in the past"));
            frappe.validated = false;
        }
    },

	refresh: function(frm) {
        frm.fields_dict.capacity.$input.on('change', function() {
            var capacity = frm.doc.capacity;

            frappe.call({
                method: 'restaurant1.Services.rest.get_available_tables',
                args: {
                    capacity: capacity
                },
                callback: function(response) {
                    var tableOptions = response.message;
                    frm.set_df_propeerty('table_fieldname', 'options', tableOptions);
                }
            });
        }) ;
        

        if (frm.doc.status === "Pending") {
            frm.add_custom_button(__('Confirm Reservation'), function() {
                frappe.call({
                    method: 'restaurant1.Services.rest.confirm_reservation',
                    args: {
                        reservation_id: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message.success) {
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('Failed to confirm reservation: ') + response.message.error);
                        }
                    }
                });
            }).addClass('btn-primary');
        }
        if (frm.doc.status === "Confirmed" || frm.doc.status === "Checked-in") {
            frm.add_custom_button(__('Mark as Completed'), function() {
                frappe.call({
                    method: 'restaurant1.Services.rest.mark_as_completed',
                    args: {
                        reservation_id: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message.success) {
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('Failed to complete reservation: ') + response.message.error);
                        }
                    }
                });
            }).addClass('btn-success');

            frm.add_custom_button(__('Mark as No-Show'), function() {
                frappe.call({
                    method: 'restaurant1.Services.rest.mark_as_no_show',
                    args: {
                        reservation_id: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message.success) {
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('Failed to mark reservation as no-show: ') + response.message.error);
                        }
                    }
                });
            }).addClass('btn-danger');

            frm.add_custom_button(__('Cancel Reservation'), function() {
                frappe.call({
                    method: 'restaurant1.Services.rest.cancel_reservation',
                    args: {
                        reservation_id: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message.success) {
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('Failed to cancel reservation: ') + response.message.error);
                        }
                    }
                });
            }).addClass('btn-warning');

            frm.add_custom_button(__('Add Preferences'), function() {
                frappe.prompt([
                    {
                        fieldname: 'preferences',
                        fieldtype: 'Small Text',
                        label: 'Preferences',
                        reqd: 1
                    }
                ], function(values) {
                    frappe.call({
                        method: 'restaurant1.Services.rest.add_preferences',
                        args: {
                            reservation_id: frm.doc.name,
                            preferences: values.preferences
                        },
                        callback: function(response) {
                            if (response.message.success) {
                                frappe.msgprint(__('Preferences added successfully.'));
                                frm.reload_doc();
                            } else {
                                frappe.msgprint(__('Failed to add preferences: ') + response.message.error);
                            }
                        }
                    });
                }, __('Add Preferences'), __('Add'));
            }).addClass('btn-primary');
        }
	},
});
