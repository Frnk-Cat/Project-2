from tkinter import *
from tkinter import ttk
import barber_shop as b

def refresh_customerlist(scrollable_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY id")
    rows = cursor.fetchall()
    header_label = Label(
                scrollable_frame,
                text=f"{'ID':<12}{'Barber ID':<18} {'Customer Name':<25} {'Service':<17} {'Date'}",
                bg=b.FRAME_COLOR,
                anchor="w",
                font=("Consolas", 10, "bold"),
                fg=b.BACKGROUND_COLOR
            )
    header_label.grid(row=0, column=0, padx=10, pady=[8,8], sticky="w", columnspan=5)
    for idx, row in enumerate(rows, start=1):
        customer_id, barber_id, customer_name, service ,date = row

        client_label = Label(
        scrollable_frame,
        text=f"{customer_id:<14} {barber_id:<16} {customer_name:<24} {service:<15} {str(date):<5}",
        bg=b.FRAME_COLOR,
        anchor="w",
        font=("Consolas", 10),
        fg=b.BACKGROUND_COLOR
        )
        client_label.grid(row=idx, column=0, padx=10, pady=2, sticky="w")  
    
    conn.close()



def customerlist_window(window):
    window = Toplevel(window)
    window.geometry("700x525")
    window.configure(bg="#303841")
    window.title("Customer list")

    canvas = Canvas(window, bg=b.BACKGROUND_COLOR , height=525, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_text(42.0, 24.0, anchor="nw", text="Customer list", fill=b.TEXT_COLOR, font=("Poppins Light", 30 * -1))

    # Add Scrollable Frame for Customers
    clients_canvas = Canvas(window, bg=b.FRAME_COLOR, bd=0, highlightthickness=0, height=519, width=862)
    clients_canvas.place(x=0, y=80, width=861, height=400)

    scrollbar = Scrollbar(window, orient=VERTICAL, bg=b.SCROLLBAR_COLOR, command=clients_canvas.yview)
    scrollbar.place(x=680, y=80, height=400, width=20)

    customer_scrollable_frame = Frame(clients_canvas, bg=b.FRAME_COLOR)
    customer_scrollable_frame.bind("<Configure>", lambda e: clients_canvas.configure(scrollregion=clients_canvas.bbox("all")))
    clients_canvas.create_window((30, 0), window=customer_scrollable_frame, anchor="nw")
    clients_canvas.configure(yscrollcommand=scrollbar.set)

    refresh = Button(
        window,
        text="⟳",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: refresh_customerlist(customer_scrollable_frame),
        fg="white",
        background=b.BUTTON_COLOR,
        activebackground=b.BUTTON_ACTIVE_COLOR,
        activeforeground="white"
    )
    refresh.place(x=610, y=29.0, width=40.0, height=35.0)

    refresh_customerlist(customer_scrollable_frame)
    window.resizable(False, False)