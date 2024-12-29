from tkinter import *
from tkinter import messagebox
import barber_shop as b
import customerlist as c
from datetime import date


# Add Barber
def add_barber(name, contact, window, scrollable_frame, label):
    
    conn = b.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO barbers (name, total_customers, contact) VALUES (%s, %s, %s)", (name, 0, contact))
    conn.commit()
    conn.close()
    c.refresh_customerlist(scrollable_frame)
    b.refresh_barber_list(window, scrollable_frame,label)
    messagebox.showinfo("Success", "Barber added successfully")

def reset_barber(window, scrollable_frame, label):
    if messagebox.askokcancel("Warning", "Are you sure you want to reset earnings?"):
        conn = b.connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, contact, earnings FROM barbers")
            rows = cursor.fetchall()

            # Calculate total income
            income = 0
            for row in rows:
                income += row[3]  # Add the earnings (4th column in the row tuple)

            # Insert total income into the income table
            cursor.execute("INSERT INTO income (day_income, date) VALUES (%s, %s)", (income, date.today()))

            # Prepare data for barber_income table
            barber_income_data = [
                (row[0], row[1], row[2], row[3], date.today()) for row in rows
            ]

            # Insert data into barber_income table
            cursor.executemany(
                "INSERT INTO barber_income (barber_id, barber_name, contact, income, date) VALUES (%s, %s, %s, %s, %s)",
                barber_income_data,
            )

            # Reset earnings and customers in barbers table
            cursor.execute(
                "UPDATE barbers SET earnings = 0, total_customers = 0"
            )

            # Delete all customers
            cursor.execute("DELETE FROM `customers`")

            # Commit the transaction
            conn.commit()

            # Refresh UI
            b.refresh_barber_list(window, scrollable_frame, label)
            messagebox.showinfo("Success", "Barber has been reset")

        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()  # Rollback in case of error

        finally:
            cursor.close()
            conn.close()



def logout(window):
    if messagebox.askokcancel("Notice", "Are sure you want to log out?"):
        try:
            conn = b.connect_to_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE user_admin SET is_login = 0 WHERE is_login = 1")
            messagebox.showinfo("Success", "Succesfully Logged Out")
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()  # Rollback in case of error
    
        finally:
            cursor.close()
            conn.close()
            window.destroy()