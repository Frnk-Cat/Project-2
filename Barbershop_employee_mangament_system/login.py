from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from barber_shop import *


def login_ui():

    def login():
        username = entry_1.get().strip()  # Remove extra whitespace
        password = password_entry.get().strip()
    
        # Check for empty fields
        if not username or not password:
            messagebox.showerror("Login error", "Please provide both Username and Password.")
            return
    
        conn = connect_to_db()
        cursor = conn.cursor()
    
        try: 
            # Query the database for user credentials
            cursor.execute(
                "SELECT username, password, is_login FROM user_admin WHERE username = %s AND password = %s LIMIT 1",
                (username, password)
            )
            result = cursor.fetchone()
    
            if result:
                stored_username, stored_password, is_login = result
    
                # Check if the user is already logged in
                if is_login:
                    messagebox.showinfo("Login Info", "User is already logged in.")
                else:
                    # Mark the user as logged in
                    cursor.execute("UPDATE user_admin SET is_login = 1 WHERE username = %s", (stored_username,))
                    conn.commit()
    
                    # Redirect to the main window
                    window.destroy()
                    main_window()
            else:
                messagebox.showerror("Login error", "Incorrect Username or Password.")
    
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()  # Rollback in case of error
    
        finally:
            cursor.close()
            conn.close()

        


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


    window = Tk()
    window.geometry("400x420")
    window.configure(bg="#303841")
    window.title("Login Window")

    canvas = Canvas(
        window,
        bg=BACKGROUND_COLOR,
        height=425,
        width=425,
        bd=0,
        highlightthickness=0
    )
    canvas.place(x=0, y=0)

    canvas.create_text(
        78.0,
        55.0,
        anchor="nw",
        text="welcome back!",
        fill="#FFFFFF",
        font=("Poppins Light", 25)
    )

    style = ttk.Style()
    style.configure("TEntry", padding=(20, 0, 20, 0))  

    # Username Entry with left padding
    username_placeholder = "Username"
    entry_1 = ttk.Entry(
        window,
        style="TEntry",
        foreground="#AAAAAA",
        font = ("Poppins Light",10)
    )
    entry_1.insert(0, username_placeholder)
    entry_1.bind("<FocusIn>", lambda event: clear_placeholder(event, username_placeholder, entry_1))
    entry_1.bind("<FocusOut>", lambda event: add_placeholder(event, username_placeholder, entry_1))
    entry_1.place(
        x=90.0,
        y=134.0,
        width=220.0,
        height=45.0
    )

    password_placeholder = "Password"
    password_entry = ttk.Entry(
        window,
        style="TEntry",
        foreground="#AAAAAA",
        font = ("Poppins Light",10)
    )
    password_entry.insert(0, password_placeholder)
    password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, password_placeholder, password_entry, is_password=True))
    password_entry.bind("<FocusOut>", lambda event: add_placeholder(event, password_placeholder, password_entry, is_password=True))
    password_entry.place(
        x=90.0,
        y=196.0,
        width=220.0,
        height=45.0
    )

    button_1 = Button(
        text="Login",
        borderwidth=0,
        highlightthickness=0,
        fg = "white",
        command=login,
        background=BUTTON_COLOR,
        relief="flat",
        activebackground=BUTTON_ACTIVE_COLOR,
        activeforeground=TEXT_COLOR,
        font = ("Poppins Light",12)
    )
    button_1.place(
        x=90.0,
        y=289.0,
        width=220.0,
        height=51.0
    )
    
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT is_login FROM user_admin")
    rows = cursor.fetchall()
    for row in rows:
        if row[0] == 1:
            main_window()
            break
    else:
        login_ui()


    
