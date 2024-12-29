from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from datetime import date
import services as serv
import customerlist as c
import mainbuttons as mainb
import frame_buttons as fb

FONT = "Consolas"
BACKGROUND_COLOR = "#17252A"        # Dark Teal
BUTTON_COLOR = "#2B7A78"            # Teal Green
BUTTON_ACTIVE_COLOR = "#3AAFA9"     # Light Teal
TEXT_COLOR = "#FEFFFF"              # White
FRAME_COLOR = "#DEF2F1"             # Light Pastel Blue
SCROLLBAR_COLOR = "#3AAFA9"
ACTIVE_BUTTON_FRAME = "#e1eded"         # Light Teal (to match buttons)


def add_edit_barber_window(window, scrollable_frame, id, option,label):

    def submit():
        name = name_entry.get()
        name = name.split()[0]
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
            mainb.add_barber(name, contact, window, scrollable_frame, label)          
        elif option == "Edit":
            fb.edit_barber(name, contact, id ,window, scrollable_frame, label)
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
    add_window.configure(bg=BACKGROUND_COLOR)
    if option == "Edit":
        add_window.title("Edit Barber")
        label_edit = Label(add_window, text="Edit Barber", font = ("Poppins Light", 24 * -1), bg=BACKGROUND_COLOR, fg="white")
        label_edit.place(x=49,y=30)
    else:
        add_window.title("Add Barber")
        label_add = Label(add_window, text="Add barber", font = ("Poppins Light", 24 * -1), bg=BACKGROUND_COLOR, fg="white")
        label_add.place(x=49,y=30)
        
    style = ttk.Style()
    style.configure("Custom.TEntry", padding=5)
    
    name_placeholder = "Name:"
    name_entry = ttk.Entry(add_window, font=("Poppins Light", 10), foreground="#AAAAAA", style="Custom.TEntry")
    name_entry.place(x=50, y=90, width=158, height=30)
    name_entry.insert(0, name_placeholder)
    name_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, name_placeholder, name_entry))
    name_entry.bind("<FocusOut>", lambda event: add_placeholder(event, name_placeholder, name_entry))

    # Contact Entry
    contact_placeholder = "Contact Number:"
    contact_entry = ttk.Entry(add_window, font=("Poppins Light", 10), foreground="#AAAAAA", style="Custom.TEntry")
    contact_entry.place(x=50, y=140, width=158, height=30)
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
        fg="white",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground="white",
        font=(FONT,10)

    )
    submit_button.place(x=51.0, y=200.0, width=67.0, height=37.0)

    # Cancel Button
    cancel_button = Button(
        add_window,
        text="Cancel",
        borderwidth=0,
        highlightthickness=0,
        command=add_window.destroy,
        relief="flat",
        fg="white",
        background="#ff0021",
        activebackground="#FCBE8E",
        activeforeground="white",
        font=(FONT,10)
    )
    cancel_button.place(x=140.0, y=200.0, width=67.0, height=37.0)
    
    add_window.resizable(False, False)
    add_window.mainloop()
    # Disable resizing



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
    cursor.execute("SELECT * FROM barbers ORDER BY id")
    rows = cursor.fetchall()
    # print(rows)
    header_label = Label(
                scrollable_frame,
                text=f"{'ID':<10}{'Barber':<17} {'Contact':<16} {'Earnings':<14} {'Customers':<26}  {'Actions'}",
                bg=FRAME_COLOR,
                anchor="w",
                font=("Consolas", 10, "bold")
            )
    header_label.grid(row=0, column=0, padx=10, pady=10, sticky="w", columnspan=5)
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
                    command=lambda barber_id = barber_id: fb.add_customer_window(barber_id, window, scrollable_frame,label),
                    background=FRAME_COLOR,
                    activebackground = ACTIVE_BUTTON_FRAME,
                    activeforeground="white",
                    width=5
                )
        add_button.grid(row=idx, column=1, padx=2.5, pady=2, sticky="w")
        addc_label = Label(window, text="Add customer", padx=4, bg="white", fg="black")
        add_button.bind("<Enter>", lambda event, label=addc_label, button=add_button: label.place(
            x=579,
            y=button.winfo_rooty() - window.winfo_rooty() - 25
        ))
        add_button.bind("<Leave>", lambda event, label=addc_label: label.place_forget())
        subtract_button = Button(
                    scrollable_frame,
                    text="➖",
                    relief="flat",
                    command=lambda barber_id = barber_id: fb.subtract_customer(barber_id, window, scrollable_frame,label),
                    background=FRAME_COLOR,
                    activebackground= ACTIVE_BUTTON_FRAME,
                    activeforeground="white",
                    width=5
                )
        subtract_button.grid(row=idx, column=2, padx=2.5, pady=2, sticky="w")
        sub_label = Label(window, text="Subtract customer", padx=4, bg="white", fg="black")
        subtract_button.bind("<Enter>", lambda event, label=sub_label, button=add_button: label.place(
            x=620,
            y=button.winfo_rooty() - window.winfo_rooty() - 25
        ))
        subtract_button.bind("<Leave>", lambda event, label=sub_label: label.place_forget())
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
        edit_label = Label(window, text="Edit barber", padx=4, bg="white", fg="black")
        edit_button.bind("<Enter>", lambda event, label=edit_label, button=add_button: label.place(
            x=690,
            y=button.winfo_rooty() - window.winfo_rooty() - 25
        ))
        edit_button.bind("<Leave>", lambda event, label=edit_label: label.place_forget())
        delete_button = Button(
                    scrollable_frame,
                    text="❌",
                    relief="flat",
                    background=FRAME_COLOR,
                    command=lambda barber_id = barber_id: fb.delete_barber(barber_id,window,scrollable_frame, label),
                    activebackground=ACTIVE_BUTTON_FRAME,
                    activeforeground="white",
                    width=5
                )
        delete_button.grid(row=idx, column=4, padx=2.5, pady=2, sticky="w")
        del_label = Label(window, text="Delete barber", padx=4, bg="white", fg="black")
        delete_button.bind("<Enter>", lambda event, label=del_label, button=add_button: label.place(
            x=737,
            y=button.winfo_rooty() - window.winfo_rooty() - 25
        ))
        delete_button.bind("<Leave>", lambda event, label=del_label: label.place_forget())


    label.config(text = f"Income | ₱{balance_sum:.0f}")
    
    conn.close()
    


def main_window():
    # Main Window
    window = Tk()
    window.geometry("862x538")
    window.configure(bg=BACKGROUND_COLOR)
    window.title("Main Dashboard")

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_text(50.0, 24.0, anchor="nw", text="Admin Panel", fill=TEXT_COLOR, font=("Poppins Light", 30 * -1))

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
        command=lambda: mainb.logout(window),
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR
    )
    logout_button.place(x=729.0, y=32.0, width=82.0, height=30.0)

    buttons_frame = Frame(window, background=BACKGROUND_COLOR)
    buttons_frame.place(x=45.0, y=470.0)

    # Add Barber Button
    add_button = Button(
        buttons_frame,
        text = "➕ ",
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
    add_label = Label(window, text="Add Barber", padx=4)
    add_button.bind("<Enter>", lambda event: add_label.place(x=43,y=430))
    add_button.bind("<Leave>", lambda event: add_label.place_forget())


    # View Customers Button
    customers_view = Button(
        buttons_frame,
        text="◉◉",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: c.customerlist_window(window),
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR,
        width=5,
        height=2
    )
    customers_view.pack(side=LEFT, padx=30)
    view_label = Label(window, text="View Customers", padx=4)
    customers_view.bind("<Enter>", lambda event: view_label.place(x=109,y=430))
    customers_view.bind("<Leave>", lambda event: view_label.place_forget())

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
        command=lambda: mainb.reset_barber(window, scrollable_frame, balance_label),
        width=5,
        height=2
    )
    reset_button.pack(side=LEFT, padx=[10,30])
    reset_label = Label(window, text="Reset Earnings", padx=4)
    reset_button.bind("<Enter>", lambda event: reset_label.place(x=194,y=430))
    reset_button.bind("<Leave>", lambda event: reset_label.place_forget())
    
    services_button = Button(
        buttons_frame,
        text="Services",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: serv.service_window(window),
        relief="flat",
        background=BUTTON_COLOR,
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        fg=TEXT_COLOR,
        width=12,
        height=2
    )
    services_button.pack(side=LEFT, padx=10)
    service_label = Label(window, text="View Services", padx=4)
    services_button.bind("<Enter>", lambda event: service_label.place(x=295,y=430))
    services_button.bind("<Leave>", lambda event: service_label.place_forget())

    # Balance Label
    balance_label = Label(text="Income | ₱0", background=BUTTON_COLOR, fg=TEXT_COLOR)
    balance_label.place(x=620.0, y=470.0, width=194.0, height=38.0)

    refresh_barber_list(window, scrollable_frame, balance_label)


    window.resizable(False, False)
    window.mainloop()
    
if __name__ == "__main__":
    main_window()
    


