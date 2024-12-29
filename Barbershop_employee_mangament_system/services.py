from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import barber_shop as b



def collect_services_amount():
    amounts = []
    services = []
    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services ORDER BY id")
    rows = cursor.fetchall()
    for id,row in enumerate(rows, start=1):
        amounts.append(float(row[2]))
        services.append(row[1])
    return amounts, services

def add_service(service, price, window, scrollable_frame):
    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (service, price) VALUES (%s, %s)", (service,price))
    conn.commit()
    conn.close()
    refresh_services(window, scrollable_frame)
    b.messagebox.showinfo("Success", "Service added successfully")
    window.deiconify()
    

def edit_service(service,price, window, scrollable_frame, id):
    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE services SET service = %s, price = %s WHERE id = %s",
        (service, price, id)
    )
    window.deiconify()
    refresh_services(window, scrollable_frame)
     
    conn.commit()
    conn.close()

    b.messagebox.showinfo("Success", "Service details updated successfully")
    window.deiconify()



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
        try:
            price = float(price)  # Try converting price to float
        except ValueError:  # Handle the case where price is not a number
            messagebox.showerror("Error", "Price must be a valid number (e.g., 10 or 10.5)")
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
    add_service_window.configure(bg=b.BACKGROUND_COLOR)
    add_service_window.title("Service List")

    style = ttk.Style()
    style.configure("Custom.TEntry", padding=5)

    if option == "Add service":
        label = Label(add_service_window, text="Add Service", font=("Poppins Light", 24 * -1), bg=b.BACKGROUND_COLOR, fg="white")
    elif option == "Edit service":
        label = Label(add_service_window, text="Edit Service", font=("Poppins Light", 24 * -1), bg=b.BACKGROUND_COLOR, fg="white")


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
        background=b.BUTTON_COLOR,
        activebackground=b.BUTTON_ACTIVE_COLOR,
        activeforeground="white",
        font=(b.FONT, 10)

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
        font=(b.FONT, 10)
    )
    cancel_button.place(x=140.0, y=200.0, width=67.0, height=37.0)

    add_service_window.resizable(False, False)


def delete_service(id,window,scrollable_frame):
    if messagebox.askokcancel("Warning", "Are you sure you want to delete this service?"):
        conn = b.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        refresh_services(window, scrollable_frame)
        messagebox.showinfo("Success", "Service has been deleted")
        window.deiconify()





def refresh_services(window, scrollable_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services ORDER BY id")

    rows = cursor.fetchall()

    header_label = Label(
        scrollable_frame,
        text=f"{'ID':<15}{'Service':<20} {'Price':<17} {'Actions'}",
        bg=b.FRAME_COLOR,
        anchor="w",
        font=("Consolas", 10, "bold")
    )
    header_label.grid(row=0, column=0, padx=10, pady=[5,10], sticky="w", columnspan=5)

    for idx, row in enumerate(rows, start=1):
        id, service, price = row
        client_label = Label(
            scrollable_frame,
            text=f"{id:<14} {service:<19}  ₱{price:<11}",
            bg=b.FRAME_COLOR,
            anchor="w",
            font=("Consolas", 10)
        )
        client_label.grid(row=idx, column=0, padx=10, pady=2, sticky="w")

        edit_button = Button(
            scrollable_frame,
            text="✏️",
            relief="flat",
            background=b.FRAME_COLOR,
            activebackground=b.ACTIVE_BUTTON_FRAME,
            command=lambda id=id: add_edit_service_window(window,scrollable_frame,"Edit service", id),
            activeforeground="white",
            width=5
        )
        edit_button.grid(row=idx, column=3, padx=2.5, pady=2, sticky="w")
        
        edit_label = Label(window, text="Edit service", padx=4, bg="white", fg="black")
        edit_button.bind("<Enter>", lambda event, label=edit_label, button=edit_button: label.place(
            x=390,
            y=button.winfo_rooty() - window.winfo_rooty() - 25
        ))
        edit_button.bind("<Leave>", lambda event, label=edit_label: label.place_forget())

        delete_button = Button(
            scrollable_frame,
            text="❌",
            relief="flat",
            background=b.FRAME_COLOR,
            command= lambda id = id: delete_service(id,window, scrollable_frame),
            activebackground=b.ACTIVE_BUTTON_FRAME,
            activeforeground="white",
            width=5
        )
        delete_button.grid(row=idx, column=4, padx=2.5, pady=2, sticky="w")
        
        del_label = Label(window, text="Delete service", padx=4, bg="white", fg="black")
        delete_button.bind("<Enter>", lambda event, label=del_label, button=delete_button: label.place(
            x=435,
            y=button.winfo_rooty() - window.winfo_rooty() - 25
        ))
        delete_button.bind("<Leave>", lambda event, label=del_label: label.place_forget())



def service_window(window):
    # Main Window
    service = Toplevel(window)
    service.geometry("550x500")
    service.configure(bg=b.BACKGROUND_COLOR)
    service.title("Main Dashboard")
    
    # Bring the window to the front
    service.attributes('-topmost', True)
    
    # Ensure it stays in front initially and then resets the "topmost" attribute
    service.after(100, lambda: service.attributes('-topmost', False))

    canvas = Canvas(service, bg=b.BACKGROUND_COLOR, height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_text(42.0, 24.0, anchor="nw", text="Services", fill=b.TEXT_COLOR, font=("Poppins Light", 30 * -1))

    # Add Scrollable Frame for Barbers
    clients_canvas = Canvas(service, bg=b.FRAME_COLOR, bd=0, highlightthickness=0, height=519, width=862)
    clients_canvas.place(x=0, y=80, width=861, height=360)

    scrollbar = Scrollbar(service, orient=VERTICAL, command=clients_canvas.yview, bg=b.SCROLLBAR_COLOR)
    scrollbar.place(x=528, y=80, height=359, width=20)

    scrollable_frame = Frame(clients_canvas, bg=b.FRAME_COLOR)
    scrollable_frame.bind("<Configure>", lambda e: clients_canvas.configure(scrollregion=clients_canvas.bbox("all")))
    clients_canvas.create_window((40, 0), window=scrollable_frame, anchor="nw")
    clients_canvas.configure(yscrollcommand=scrollbar.set)

    # Log Out Button
    add_service_button = Button(
        service,
        text="➕ ",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        background=b.BUTTON_COLOR,
        activebackground=b.BUTTON_ACTIVE_COLOR,
        activeforeground=b.TEXT_COLOR,
        command=lambda: add_edit_service_window(service, scrollable_frame, "Add service"),
        fg=b.TEXT_COLOR,
        width=5,
        height=2
    )
    add_service_button.place(x=450.0, y=27.0)
    
    add_label = Label(service, text="Add service", padx=4, bg="white", fg="black")
    add_service_button.bind("<Enter>", lambda event, label=add_label, button=add_service_button: label.place(
        x=433,
        y=4
    ))
    add_service_button.bind("<Leave>", lambda event, label=add_label: label.place_forget())

    refresh_services(service, scrollable_frame)
    service.resizable(False, False)

    
