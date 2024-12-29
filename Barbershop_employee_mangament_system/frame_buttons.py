from tkinter import *
from tkinter import messagebox
import barber_shop as b
import customerlist as c
import services as serv
from datetime import date
from tkinter import ttk


def delete_barber(barber_id,window,scrollable_frame, label):
    if messagebox.askokcancel("Warning", "Are you sure you want to delete this barber?"):
        conn = b.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM barbers WHERE id = %s", (barber_id,))
        cursor.execute("DELETE FROM customers WHERE barber_id = %s", (barber_id,))
        conn.commit()
        conn.close()
        c.refresh_customerlist(scrollable_frame)
        b.refresh_barber_list(window, scrollable_frame, label)
        messagebox.showinfo("Success", "Baber has been deleted")




def subtract_customer(barber_id, window, scrollable_frame, label):
    if messagebox.askokcancel("Warning", "Do you wish to continue?"):
        conn = b.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT earnings FROM barbers WHERE id = %s", (barber_id,))
        if cursor.fetchone() == 0:
            messagebox.showinfo("Error", "Can't subtract any furthur.")
            return
        # Fetch the last customer for the barber
        cursor.execute(
            "SELECT * FROM customers WHERE barber_id = %s ORDER BY id DESC LIMIT 1",
            (barber_id,)
        )
        last_customer = cursor.fetchone()
        if last_customer:
            last_customer_service = last_customer[3]
            # Delete the last customer
            cursor.execute(
                "DELETE FROM customers WHERE id = %s ORDER BY id DESC LIMIT 1",
                (last_customer[0],)
            )

            # Decrement the total_customers count
            cursor.execute(
                "UPDATE barbers SET total_customers = total_customers - 1 WHERE id = %s",
                (barber_id,)
            )
            amounts, services = serv.collect_services_amount()
            for x, s in enumerate(services, start=0):
                if s == last_customer_service:
                    cursor.execute("UPDATE barbers SET earnings = earnings - %s WHERE id = %s", 
                                (amounts[x], barber_id)
                                )

            conn.commit()
            b.refresh_barber_list(window, scrollable_frame, label)
            messagebox.showinfo("Success", "Customer removed successfully.")
        else:
            messagebox.showinfo("Info", "No customers to remove for this barber.")

        conn.close()


# Edit Barber
def edit_barber(new_name, new_contact, barber_id, window, scrollable_frame, label):

    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE barbers SET name = %s, contact = %s WHERE id = %s",
        (new_name, new_contact, barber_id)
    )
    conn.commit()
    conn.close()
    c.refresh_customerlist(scrollable_frame)
    b.refresh_barber_list(window, scrollable_frame, label)
    messagebox.showinfo("Success", "Barber details updated successfully")


# Add Customer to Barber
def add_customer(barber_id, name, service, window, scrollable_frame, label):
    amounts, services = serv.collect_services_amount()   
    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (barber_id, customers_name, service, date) VALUES (%s, %s, %s, %s)",
        (barber_id, name, service, date.today(),)
    )
    cursor.execute(
        "UPDATE barbers SET total_customers = total_customers + 1 WHERE id = %s", 
        (barber_id,)
    )
    for x, s in enumerate(services, start=0):
        if s == service:
            cursor.execute("UPDATE barbers SET earnings = earnings + %s WHERE id = %s", (amounts[x], barber_id))
    
    conn.commit()
    conn.close()
    b.refresh_barber_list(window,scrollable_frame,label)
    messagebox.showinfo("Success", "Customer tracked successfully")
    
    

def add_customer_window(barber_id, window, scrollable_frame, label):
    def submit(placeholder):
        service = service_option.get()
        name = name_entry.get()
        if name == placeholder or not name:
            messagebox.showerror("Input Error", "Customer's name is required")
            return
        customer.destroy()
        add_customer(barber_id, name, service, window, scrollable_frame, label)

    def clear_placeholder(event, placeholder_text, entry_widget):
        """Clear the placeholder text if it matches the current content."""
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, END)
            entry_widget.config(foreground="#000000")


    def add_placeholder(event, placeholder_text, entry_widget):
        """Restore the placeholder text if the entry is empty."""
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder_text)
            entry_widget.config(foreground="#AAAAAA")

    customer = Toplevel(window)
    customer.geometry("256x320")
    customer.configure(bg=b.BACKGROUND_COLOR)
    customer.title("Add Customer")

    add_label = Label(customer, text="Add Customer", font = ("Poppins Light", 24 * -1), bg=b.BACKGROUND_COLOR, fg="white")
    add_label.place(x=45,y=30)
    
    name_placeholder = "Customer's Name:"
    name_entry = ttk.Entry(customer, font=("Poppins Light", 10), foreground="#AAAAAA")
    name_entry.place(x=50, y=90, width=158, height=30)
    name_entry.insert(0, name_placeholder)
    name_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, name_placeholder, name_entry))
    name_entry.bind("<FocusOut>", lambda event: add_placeholder(event, name_placeholder, name_entry))

    # Contact Entry
    amounts, services = serv.collect_services_amount()   
    service_option = ttk.Combobox(customer, state="readonly", values=services,font=("Poppins Light", 10), foreground="black")
    service_option.place(x=50, y=140, width=158, height=30)
    service_option.set(services[0])


    submit_button = Button(
        customer,
        text="Save",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: submit(name_placeholder),
        relief="flat",
        fg= "white",
        background=b.BUTTON_COLOR,
        activebackground=b.BUTTON_ACTIVE_COLOR,
        activeforeground="white",
        font= (b.FONT,10)
    )
    submit_button.place(x=51.0, y=200.0, width=67.0, height=37.0)

    # Cancel Button
    cancel_button = Button(
        customer,
        text="Cancel",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        fg="white",
        command=customer.destroy,
        background="#ff0021",
        activebackground="#FCBE8E",
        activeforeground="white",
        font=(b.FONT,10)
    )
    cancel_button.place(x=140.0, y=200.0, width=67.0, height=37.0)
    customer.resizable(False, False)