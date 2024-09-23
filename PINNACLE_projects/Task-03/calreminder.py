import calendar
import json
from tkinter import Tk, Label, Button, Entry, Listbox, Toplevel, messagebox, END, StringVar, Frame
import datetime
import threading
import time
import os

reminders = {}

reminders_file = "reminders.json"

def load_reminders():
    global reminders
    if os.path.exists(reminders_file):
        with open(reminders_file, 'r') as f:
            reminders = json.load(f)

def save_reminders():
    with open(reminders_file, 'w') as f:
        json.dump(reminders, f)

def display_calendar(year, month):
    cal_text = calendar.month(year, month) 
    calendar_label.config(text=cal_text) 

def next_month():
    global current_month, current_year
    if current_month == 12:
        current_month = 1
        current_year += 1
    else:
        current_month += 1
    display_calendar(current_year, current_month)

def previous_month():
    global current_month, current_year
    if current_month == 1:
        current_month = 12
        current_year -= 1
    else:
        current_month -= 1
    display_calendar(current_year, current_month)

def manage_reminders():
    def refresh_reminder_list(date):
        if date in reminders:
            reminder_list.delete(0, END)
            for reminder in reminders[date]:
                reminder_list.insert(END, reminder)
        else:
            reminder_list.delete(0, END)
            reminder_list.insert(END, "No reminders for this date.")

    def save_new_reminder():
        date = date_entry.get()
        reminder_text = reminder_entry.get()

        if date and reminder_text:
            if date not in reminders:
                reminders[date] = []
            reminders[date].append(reminder_text)
            messagebox.showinfo("Success", f"Reminder added for {date}!")
            save_reminders()  # Save the reminders to file
            refresh_reminder_list(date)
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def delete_selected_reminder():
        date = date_entry.get()
        selected = reminder_list.curselection()
        if selected:
            reminder_text = reminder_list.get(selected)
            reminders[date].remove(reminder_text)
            if not reminders[date]:
                del reminders[date]
            messagebox.showinfo("Success", "Reminder deleted!")
            save_reminders()
            refresh_reminder_list(date)
        else:
            messagebox.showwarning("Error", "Please select a reminder to delete.")

    def edit_selected_reminder():
        date = date_entry.get()
        selected = reminder_list.curselection()
        if selected:
            reminder_text = reminder_list.get(selected)
            reminder_entry.delete(0, END)
            reminder_entry.insert(0, reminder_text)

            def update_reminder():
                new_text = reminder_entry.get()
                if new_text:
                    reminders[date].remove(reminder_text)
                    reminders[date].append(new_text)
                    save_reminders()
                    refresh_reminder_list(date)
                    messagebox.showinfo("Success", "Reminder updated!")
                    edit_button.config(state="normal")
                    add_button.config(text="Add Reminder", command=save_new_reminder)
                    reminder_entry.delete(0, END)

            add_button.config(text="Update Reminder", command=update_reminder)
            edit_button.config(state="disabled")
        else:
            messagebox.showwarning("Error", "Please select a reminder to edit.")

    manage_window = Toplevel(root)
    manage_window.title("Manage Reminders")
    manage_window.geometry("400x400")

    Label(manage_window, text="Enter Date (YYYY-MM-DD):").pack(pady=10)
    date_entry = Entry(manage_window)
    date_entry.pack(pady=5)

    Label(manage_window, text="Enter Reminder:").pack(pady=10)
    reminder_entry = Entry(manage_window)
    reminder_entry.pack(pady=5)

    reminder_list = Listbox(manage_window)
    reminder_list.pack(pady=20)

    add_button = Button(manage_window, text="Add Reminder", command=save_new_reminder)
    add_button.pack(pady=5)

    edit_button = Button(manage_window, text="Edit Selected Reminder", command=edit_selected_reminder)
    edit_button.pack(pady=5)

    delete_button = Button(manage_window, text="Delete Selected Reminder", command=delete_selected_reminder)
    delete_button.pack(pady=5)

    def on_date_change(*args):
        refresh_reminder_list(date_entry.get())

    date_entry_var = StringVar()
    date_entry.config(textvariable=date_entry_var)
    date_entry_var.trace("w", on_date_change)

def check_today_reminders():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if today in reminders:
        reminder_list = "\n".join(reminders[today])
        messagebox.showinfo("Today's Reminders", f"Today's reminders:\n{reminder_list}")
    else:
        messagebox.showinfo("Today's Reminders", "No reminders for today.")

def reminder_notifier():
    while True:
        check_today_reminders()
        time.sleep(600)

current_year = 2024
current_month = 9

root = Tk()
root.title("Calendar and Reminder App")
root.geometry("400x350")

calendar_label = Label(root, text="", font=("Courier", 12))
calendar_label.pack(pady=10)
display_calendar(current_year, current_month)

prev_button = Button(root, text="Previous", command=previous_month)
prev_button.pack(side="left", padx=20)

next_button = Button(root, text="Next", command=next_month)
next_button.pack(side="right", padx=20)

manage_reminders_button = Button(root, text="Manage Reminders", command=manage_reminders)
manage_reminders_button.pack(pady=10)

today_reminders_button = Button(root, text="Check Today's Reminders", command=check_today_reminders)
today_reminders_button.pack(pady=10)

load_reminders()

notifier_thread = threading.Thread(target=reminder_notifier, daemon=True)
notifier_thread.start()

root.mainloop()