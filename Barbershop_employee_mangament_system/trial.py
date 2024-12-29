from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from datetime import date
from tkinter import font

ACTIVE_BUTTON_FRAME = "#e1eded"         # Light Teal (to match buttons)
FONT = "Consolas"

# amounts = [50,30]
# services = ["Haircut", "Shave"]
# Define global theme variable
is_dark_mode = False

# Toggle dark mode
def toggle_dark_mode(window, scrollable_frame):
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    update_theme(window, scrollable_frame)

# Update theme
def update_theme(window, scrollable_frame):
    global is_dark_mode
    
    # Define dark mode colors
    dark_bg = "#303841"
    dark_fg = "#FFFFFF"
    light_bg = "#FFFFFF"
    light_fg = "#000000"
    button_color = "#48CFCB"
    active_button_color = "#91DDCF"

    # Apply colors based on the theme
    bg_color = dark_bg if is_dark_mode else light_bg
    fg_color = dark_fg if is_dark_mode else light_fg
    btn_color = button_color if is_dark_mode else "#CCCCCC"
    active_btn_color = active_button_color if is_dark_mode else "#AAAAAA"

    window.configure(bg=bg_color)
    for widget in window.winfo_children():
        if isinstance(widget, Label):
            widget.configure(bg=bg_color, fg=fg_color)
        elif isinstance(widget, Button):
            widget.configure(bg=btn_color, fg=fg_color, activebackground=active_btn_color, activeforeground=fg_color)
        elif isinstance(widget, Canvas):
            widget.configure(bg=bg_color)
        elif isinstance(widget, Frame):
            widget.configure(bg=bg_color)
        elif isinstance(widget, Scrollbar):
            widget.configure(bg=bg_color)

    # Update scrollable frame
    scrollable_frame.configure(bg=bg_color)
    refresh_barber_list(window, scrollable_frame, None)  # Refresh lists to apply colors


def refresh_customerlist(scrollable_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY id")
    rows = cursor.fetchall()
    header_label = Label(
                scrollable_frame,
                text=f"{'ID':<6}{'Barber ID':<15} {'Customers Name':<30} {'Service':<18} {'Date'}",
                bg="#D9D9D9",
                anchor="w",
                font=("Courier", 10, "bold"),
                fg="white"
            )
    header_label.grid(row=0, column=0, padx=10, pady=2, sticky="w", columnspan=5)
    for idx, row in enumerate(rows, start=1):
        customer_id, barber_id, customer_name, service ,date= row

        client_label = Label(
        scrollable_frame,
        text=f"{customer_id:<8} {barber_id:<12} {customer_name:<30} {service:<15} {str(date):<5}",
        bg="#D9D9D9",
        anchor="w",
        font=("Courier", 10)
        )
        client_label.grid(row=idx, column=0, padx=10, pady=2, sticky="w")  
    
    conn.close()



def customerlist_window(window):
    window = Toplevel(window)
    window.geometry("700x525")
    window.configure(bg="#303841")
    window.title("Customer list")

    canvas = Canvas(window, bg="#303841", height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_text(42.0, 24.0, anchor="nw", text="Customer list", fill="#FFFFFF", font=("Poppins Light", 30 * -1))

    # Add Scrollable Frame for Barbers
    clients_canvas = Canvas(window, bg="#D9D9D9", bd=0, highlightthickness=0, height=519, width=862)
    clients_canvas.place(x=0, y=80, width=861, height=400)

    scrollbar = Scrollbar(window, orient=VERTICAL, command=clients_canvas.yview)
    scrollbar.place(x=680, y=80, height=400, width=20)

    customer_scrollable_frame = Frame(clients_canvas, bg="#D9D9D9")
    customer_scrollable_frame.bind("<Configure>", lambda e: clients_canvas.configure(scrollregion=clients_canvas.bbox("all")))
    clients_canvas.create_window((11, 0), window=customer_scrollable_frame, anchor="nw")
    clients_canvas.configure(yscrollcommand=scrollbar.set)

    refresh = Button(
        window,
        text="⟳",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: refresh_customerlist(customer_scrollable_frame),
        background="#48CFCB",
        activebackground="#91DDCF",
        activeforeground="white"
    )
    refresh.place(x=610, y=29.0, width=40.0, height=35.0)

    refresh_customerlist(customer_scrollable_frame)
    window.resizable(False, False)



# Database Connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="barbershop_db"
    )


def refresh_barber_list(window, scrollable_frame, label):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barbers")
    rows = cursor.fetchall()
    # print(rows)
    header_label = Label(
                scrollable_frame,
                text=f"{'ID':<10}{'Barber':<17} {'Contact':<16} {'Earnings':<14} {'Cutsomer':<26}  {'Actions'}",
                bg=FRAME_COLOR,
                anchor="w",
                font=("Consolas", 10, "bold")
            )
    header_label.grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=5)
    balance_sum = 0
    for idx, row in enumerate(rows, start=1):
        barber_id, name, contact, total_customers, earnings = row
        balance_sum += float(earnings)

        client_label = Label(
        scrollable_frame,
        text=f"{barber_id:<9} {name:<17} {contact:<19} ₱{earnings:<13} {total_customers:<13}",
        bg=FRAME_COLOR,
        anchor="w",
        font=("Consolas", 10)
        )
        client_label.grid(row=idx, column=0, padx=10, pady=2, sticky="w")
        add_button = Button(
                    scrollable_frame,
                    text="➕",
                    relief="flat",
                    command=lambda barber_id = barber_id: add_customer_window(barber_id, window, scrollable_frame,label),
                    background=FRAME_COLOR,
                    activebackground = ACTIVE_BUTTON_FRAME,
                    activeforeground="white",
                    width=5
                )
        add_button.grid(row=idx, column=1, padx=2.5, pady=2, sticky="w")
        subtract_button = Button(
                    scrollable_frame,
                    text="➖",
                    relief="flat",
                    command=lambda barber_id = barber_id: subtract_customer(barber_id, window, scrollable_frame,label),
                    background=FRAME_COLOR,
                    activebackground= ACTIVE_BUTTON_FRAME,
                    activeforeground="white",
                    width=5
                )
        subtract_button.grid(row=idx, column=2, padx=2.5, pady=2, sticky="w")
        edit_button = Button(
                    scrollable_frame,
                    text="✏️",
                    relief="flat",
                    background=FRAME_COLOR,
                    command=lambda barber_id = barber_id: add_edit_barber_window(window,scrollable_frame,barber_id,"Edit", label),
                    activebackground=ACTIVE_BUTTON_FRAME,
                    activeforeground="white",
                    width=5
                )
        edit_button.grid(row=idx, column=3, padx=2.5, pady=2, sticky="w")
        delete_button = Button(
                    scrollable_frame,
                    text="❌",
                    relief="flat",
                    background=FRAME_COLOR,
                    command=lambda barber_id = barber_id: delete_barber(barber_id,window,scrollable_frame, label),
                    activebackground=ACTIVE_BUTTON_FRAME,
                    activeforeground="white",
                    width=5
                )
        delete_button.grid(row=idx, column=4, padx=2.5, pady=2, sticky="w")
    label.config(text = f"Balance | ₱{balance_sum:.2f}")
    
    conn.close()



def subtract_customer(barber_id, window, scrollable_frame, label):
    if messagebox.askokcancel("Warning", "Do you wish to continue?"):
        conn = connect_to_db()
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
            for x, s in enumerate(services, start=0):
                if s == last_customer_service:
                    cursor.execute("UPDATE barbers SET earnings = earnings - %s WHERE id = %s", 
                                (amounts[x], barber_id)
                                )

            conn.commit()
            refresh_barber_list(window, scrollable_frame, label)
            messagebox.showinfo("Success", "Customer removed successfully.")
        else:
            messagebox.showinfo("Info", "No customers to remove for this barber.")

        conn.close()




# Add Barber
def add_barber(name, contact, window, scrollable_frame, label):
    name = name.split(" ")[0]
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO barbers (name, total_customers, contact) VALUES (%s, %s, %s)", (name, 0, contact))
    conn.commit()
    conn.close()
    refresh_customerlist(scrollable_frame)
    refresh_barber_list(window, scrollable_frame,label)
    messagebox.showinfo("Success", "Barber added successfully")

def add_edit_barber_window(window, scrollable_frame, id, option,label):
    def submit():
        name = name_entry.get()
        contact = contact_entry.get()
        if name == "Name:" or not name:
            messagebox.showerror("Input Error", "Barber name is required")
            return
        if contact == "Contact:" or not contact:
            messagebox.showerror("Input Error", "Barber contact is required")
            return
        if not contact.strip().isdigit():
            messagebox.showerror("Input Error","Contact must be number")
            return
        if len(contact)!= 11:
            messagebox.showerror("Input Error","Contact number must be exactly 11 numbers")
            return
        if option == "Add":
            add_barber(name, contact, window, scrollable_frame, label)          
        elif option == "Edit":
            edit_barber(name, contact, id ,window, scrollable_frame, label)
        add_window.destroy()
        
            

    def clear_placeholder(event, placeholder_text, entry_widget, is_password=False):
        """Clear the placeholder text if it matches the current content."""
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, END)
            entry_widget.config(foreground="#000000")
            if is_password:
                entry_widget.config(show="*")

    def add_placeholder(event, placeholder_text, entry_widget, is_password=False):
        """Restore the placeholder text if the entry is empty."""
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder_text)
            entry_widget.config(foreground="#AAAAAA")
            if is_password:
                entry_widget.config(show="")

    add_window = Toplevel(window)
    add_window.geometry("256x320")
    add_window.configure(bg="#303841")
    if option == "Edit":
        add_window.title("Edit Barber")
    else:
        add_window.title("Add Barber")

    name_placeholder = "Name:"
    name_entry = ttk.Entry(add_window, font=("Poppins Light", 10), foreground="#AAAAAA")
    name_entry.place(x=50, y=50, width=158, height=30)
    name_entry.insert(0, name_placeholder)
    name_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, name_placeholder, name_entry))
    name_entry.bind("<FocusOut>", lambda event: add_placeholder(event, name_placeholder, name_entry))

    # Contact Entry
    contact_placeholder = "Contact Number:"
    contact_entry = ttk.Entry(add_window, font=("Poppins Light", 10), foreground="#AAAAAA")
    contact_entry.place(x=50, y=100, width=158, height=30)
    contact_entry.insert(0, contact_placeholder)
    contact_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, contact_placeholder, contact_entry))
    contact_entry.bind("<FocusOut>", lambda event: add_placeholder(event, contact_placeholder, contact_entry))


    # Submit Button
    submit_button = Button(
        add_window,
        text="Save",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=submit,
        background="#48CFCB",
        activebackground="#91DDCF",
        activeforeground="white"
    )
    submit_button.place(x=51.0, y=216.0, width=66.0, height=37.0)

    # Cancel Button
    cancel_button = Button(
        add_window,
        text="Cancel",
        borderwidth=0,
        highlightthickness=0,
        command=add_window.destroy,
        relief="flat",
        fg="white",
        background="#D91656",
        activebackground="#FF4545",
        activeforeground="white"
    )
    cancel_button.place(x=140.0, y=216.0, width=66.0, height=37.0)
    
    add_window.resizable(False, False)
    add_window.mainloop()
    # Disable resizing
    
def add_service(service, price, window, scrollable_frame):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (service, price) VALUES (%s, %s)", (service,price))
    conn.commit()
    conn.close()
    refresh_services(window, scrollable_frame)
    messagebox.showinfo("Success", "Service added successfully")

def edit_service(service,price, window, scrollable_frame, id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE services SET service = %s, price = %s WHERE id = %s",
        (service, price, id)
    )
    refresh_services(window, scrollable_frame)
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Service details updated successfully")



def add_edit_service_window(window, scrollable_frame, option, id = None):
    def submit(service_placeholder, price_palceholder):
        service = service_entry.get().strip()
        price = price_entry.get().strip()
        if not service or service == service_placeholder:  # Check if service is empty
            messagebox.showerror("Error", "Provide a service")
            return  # Exit the function
        if price == "":
            messagebox.showerror("Error", "Provide a price")
            return

        if not price or price == price_palceholder:  # Check if price is empty
            messagebox.showerror("Error", "Provide a price")
            return  # Exit the function
        elif not price.isdigit():  # Check if price is not a number
            messagebox.showerror("Error", "Price must be a number")
            return  # Exit the function
        add_service_window.destroy()
         # If both validations pass
        if option == "Add service":
            add_service(service, price, window, scrollable_frame)
        elif option == "Edit service":
            edit_service(service,price, window, scrollable_frame, id)


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

    add_service_window = Toplevel(window)
    add_service_window.geometry("256x320")
    add_service_window.configure(bg=BACKGROUND_COLOR)
    add_service_window.title("Service List")

    style = ttk.Style()
    style.configure("Custom.TEntry", padding=5)

    if option == "Add service":
        label = Label(add_service_window, text="Add Service", font=("Poppins Light", 24 * -1), bg=BACKGROUND_COLOR, fg="white")
    elif option == "Edit service":
        label = Label(add_service_window, text="Edit Service", font=("Poppins Light", 24 * -1), bg=BACKGROUND_COLOR, fg="white")


    label.place(x=49, y=30)
    service_placeholder = "Service:"
    service_entry = ttk.Entry(add_service_window, font=("Poppins Light", 10), foreground="#AAAAAA", style="Custom.TEntry")
    service_entry.place(x=50, y=90, width=158, height=30)
    service_entry.insert(0, service_placeholder)
    service_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, service_placeholder, service_entry))
    service_entry.bind("<FocusOut>", lambda event: add_placeholder(event, service_placeholder, service_entry))

    # Contact Entry
    price_placeholder = "Price: (in pesos)"
    price_entry = ttk.Entry(add_service_window, font=("Poppins Light", 10), foreground="#AAAAAA", style="Custom.TEntry")
    price_entry.place(x=50, y=140, width=158, height=30)
    price_entry.insert(0, price_placeholder)
    price_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, price_placeholder, price_entry))
    price_entry.bind("<FocusOut>", lambda event: add_placeholder(event, price_placeholder, price_entry))

    # Submit Button
    submit_button = Button(
        add_service_window,
        text="Save",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: submit(service_placeholder,price_placeholder),
        fg="white",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground="white",
        font=(FONT, 10)

    )
    submit_button.place(x=51.0, y=200.0, width=67.0, height=37.0)

    # Cancel Button
    cancel_button = Button(
        add_service_window,
        text="Cancel",
        borderwidth=0,
        highlightthickness=0,
        command=add_service_window.destroy,
        relief="flat",
        fg="white",
        background="#ff0021",
        activebackground="#FCBE8E",
        activeforeground="white",
        font=(FONT, 10)
    )
    cancel_button.place(x=140.0, y=200.0, width=67.0, height=37.0)

    add_service_window.resizable(False, False)
    add_service_window.mainloop()


def delete_service(id,window,scrollable_frame):
    if messagebox.askokcancel("Warning", "Are you sure you want to delete this service?"):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        refresh_services(window, scrollable_frame)
        messagebox.showinfo("Success", "Service has been deleted")





def refresh_services(window, scrollable_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")

    rows = cursor.fetchall()

    header_label = Label(
        scrollable_frame,
        text=f"{'ID':<15}{'Service':<20} {'Price':<17} {'Actions'}",
        bg=FRAME_COLOR,
        anchor="w",
        font=("Consolas", 10, "bold")
    )
    header_label.grid(row=0, column=0, padx=10, pady=[5,10], sticky="w", columnspan=5)

    for idx, row in enumerate(rows, start=1):
        id, service, price = row
        client_label = Label(
            scrollable_frame,
            text=f"{id:<14} {service:<19}  ₱{price:<11}",
            bg=FRAME_COLOR,
            anchor="w",
            font=("Consolas", 10)
        )
        client_label.grid(row=idx, column=0, padx=10, pady=2, sticky="w")

        edit_button = Button(
            scrollable_frame,
            text="✏️",
            relief="flat",
            background=FRAME_COLOR,
            activebackground=ACTIVE_BUTTON_FRAME,
            command=lambda id=id: add_edit_service_window(window,scrollable_frame,"Edit service", id),
            activeforeground="white",
            width=5
        )
        edit_button.grid(row=idx, column=3, padx=2.5, pady=2, sticky="w")

        delete_button = Button(
            scrollable_frame,
            text="❌",
            relief="flat",
            background=FRAME_COLOR,
            command= lambda id = id: delete_service(id,window, scrollable_frame),
            activebackground=ACTIVE_BUTTON_FRAME,
            activeforeground="white",
            width=5
        )
        delete_button.grid(row=idx, column=4, padx=2.5, pady=2, sticky="w")



def service_window(window):
    # Main Window
    window = Toplevel(window)
    window.geometry("550x500")
    window.configure(bg=BACKGROUND_COLOR)
    window.title("Main Dashboard")

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_text(42.0, 24.0, anchor="nw", text="Services", fill=TEXT_COLOR, font=("Poppins Light", 30 * -1))

    # Add Scrollable Frame for Barbers
    clients_canvas = Canvas(window, bg=FRAME_COLOR, bd=0, highlightthickness=0, height=519, width=862)
    clients_canvas.place(x=0, y=80, width=861, height=360)

    scrollbar = Scrollbar(window, orient=VERTICAL, command=clients_canvas.yview, bg=SCROLLBAR_COLOR)
    scrollbar.place(x=528, y=80, height=359, width=20)

    scrollable_frame = Frame(clients_canvas, bg=FRAME_COLOR)
    scrollable_frame.bind("<Configure>", lambda e: clients_canvas.configure(scrollregion=clients_canvas.bbox("all")))
    clients_canvas.create_window((40, 0), window=scrollable_frame, anchor="nw")
    clients_canvas.configure(yscrollcommand=scrollbar.set)

    # Log Out Button
    add_service_button = Button(
        window,
        text="➕ ",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        command=lambda: add_edit_service_window(window, scrollable_frame, "Add service"),
        fg=TEXT_COLOR,
        width=5,
        height=2
    )
    add_service_button.place(x=450.0, y=27.0)

    refresh_services(window, scrollable_frame)

    window.resizable(False, False)


def collect_services_amount():
    amounts = []
    services = []
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services ORDER BY id")
    rows = cursor.fetchall()
    for id,row in enumerate(rows, start=1):
        amounts.append(row[2])
        services.append(row[1])
    return amounts, services

# Add Customer to Barber
def add_customer(barber_id, name, service, window, scrollable_frame, label):
    amounts, services = collect_services_amount()        
    conn = connect_to_db()
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
    refresh_barber_list(window,scrollable_frame,label)
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
    customer.geometry("256x280")
    customer.configure(bg="#303841")
    customer.title("Add Customer")

    name_placeholder = "Customer's Name:"
    name_entry = ttk.Entry(customer, font=("Poppins Light", 10), foreground="#AAAAAA")
    name_entry.place(x=50, y=50, width=158, height=30)
    name_entry.insert(0, name_placeholder)
    name_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, name_placeholder, name_entry))
    name_entry.bind("<FocusOut>", lambda event: add_placeholder(event, name_placeholder, name_entry))

    # Contact Entry
    amounts, services = collect_services_amount()   
    service_option = ttk.Combobox(customer, state="readonly", values=services,font=("Poppins Light", 10), foreground="black")
    service_option.place(x=50, y=100, width=158, height=30)
    service_option.set(services[0])


    submit_button = Button(
        customer,
        text="Save",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: submit(name_placeholder),
        relief="flat",
        background="#48CFCB",
        activebackground="#91DDCF",
        activeforeground="white"
    )
    submit_button.place(x=51.0, y=159, width=66.0, height=37.0)

    # Cancel Button
    cancel_button = Button(
        customer,
        text="Cancel",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        fg="white",
        background="#D91656",
        activebackground="#FF4545",
        activeforeground="white"
    )
    cancel_button.place(x=140.0, y=159, width=66.0, height=37.0)
    customer.resizable(False, False)



# Edit Barber
def edit_barber(new_name, new_contact, barber_id, window, scrollable_frame, label):

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE barbers SET name = %s, contact = %s WHERE id = %s",
        (new_name, new_contact, barber_id)
    )
    conn.commit()
    conn.close()
    refresh_customerlist(scrollable_frame)
    refresh_barber_list(window, scrollable_frame, label)
    messagebox.showinfo("Success", "Barber details updated successfully")


def delete_barber(barber_id,window,scrollable_frame, label):
    if messagebox.askokcancel("Warning", "Are you sure you want to delete this barber?"):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM barbers WHERE id = %s", (barber_id,))
        conn.commit()
        conn.close()
        refresh_customerlist(scrollable_frame)
        refresh_barber_list(window, scrollable_frame, label)
        messagebox.showinfo("Success", "Baber has been deleted")

def reset_barber(window,scrollable_frame, label):
    if messagebox.askokcancel("Warning", "Are you sure you want to reset earnings?"):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE barbers SET earnings = 0, total_customers = 0",
            )
        cursor.execute(
            "DELETE FROM `customers`"
            )
        conn.commit()
        conn.close()
        refresh_barber_list(window, scrollable_frame, label)
        messagebox.showinfo("Success", "Baber has been reset")


BACKGROUND_COLOR = "#17252A"        # Dark Teal
BUTTON_COLOR = "#2B7A78"            # Teal Green
BUTTON_ACTIVE_COLOR = "#3AAFA9"     # Light Teal
TEXT_COLOR = "#FEFFFF"              # White
FRAME_COLOR = "#DEF2F1"             # Light Pastel Blue
SCROLLBAR_COLOR = "#3AAFA9"         # Light Teal (to match buttons)

def main_window():
    # Main Window
    window = Tk()
    window.geometry("862x519")
    window.configure(bg=BACKGROUND_COLOR)
    window.title("Main Dashboard")

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_text(42.0, 24.0, anchor="nw", text="Admin Panel", fill=TEXT_COLOR, font=("Poppins Light", 30 * -1))

    # Add Scrollable Frame for Barbers
    clients_canvas = Canvas(window, bg=FRAME_COLOR, bd=0, highlightthickness=0, height=519, width=862)
    clients_canvas.place(x=0, y=80, width=861, height=360)

    scrollbar = Scrollbar(window, orient=VERTICAL, command=clients_canvas.yview, bg=SCROLLBAR_COLOR)
    scrollbar.place(x=841, y=80, height=359, width=20)

    scrollable_frame = Frame(clients_canvas, bg=FRAME_COLOR)
    scrollable_frame.bind("<Configure>", lambda e: clients_canvas.configure(scrollregion=clients_canvas.bbox("all")))
    clients_canvas.create_window((40, 0), window=scrollable_frame, anchor="nw")
    clients_canvas.configure(yscrollcommand=scrollbar.set)

    # Log Out Button
    logout_button = Button(
        text="Log Out",
        borderwidth=0,
        highlightthickness=0,
        command=window.destroy,
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR
    )
    logout_button.place(x=729.0, y=32.0, width=82.0, height=30.0)

    buttons_frame = Frame(window, background=BACKGROUND_COLOR)
    buttons_frame.place(x=60.0, y=460.0)

    # Add Barber Button
    add_button = Button(
        buttons_frame,
        text="+",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: add_edit_barber_window(window, scrollable_frame, None, "Add", balance_label),
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR,
        width=5,
        height=2
    )
    add_button.pack(side=LEFT, padx=10)

    # View Customers Button
    customers_view = Button(
        buttons_frame,
        text="👁",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: customerlist_window(window),
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR,
        width=5,
        height=2
    )
    customers_view.pack(side=LEFT, padx=30)

    # Reset Button
    reset_button = Button(
        buttons_frame,
        text="↻",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR,
        command=lambda: reset_barber(window, scrollable_frame, balance_label),
        width=5,
        height=2
    )
    reset_button.pack(side=LEFT, padx=10)

    services_button = Button(
        buttons_frame,
        text="services",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: service_window(window),
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR,
        width=5,
        height=2
    )
    services_button.pack(side=LEFT, padx=10)


    # Balance Label
    balance_label = Label(text="Balance | ₱0.0", background=BUTTON_COLOR, fg=TEXT_COLOR)
    balance_label.place(x=620.0, y=463.0, width=194.0, height=38.0)

    refresh_barber_list(window, scrollable_frame, balance_label)


    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    main_window()
