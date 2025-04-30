import json
import uuid
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from jsonschema import validate, ValidationError
from json.decoder import JSONDecodeError

def generate_uuid_if_blank(value):
    return value if value.strip() else str(uuid.uuid4())

def validate_datetime(value):
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False

def submit():
    try:
        # Build datetime strings
        start_datetime = f"{start_date_entry.get()}T{start_time_combo.get()}:00"
        end_datetime = f"{end_date_entry.get()}T{end_time_combo.get()}:00"

        # Build event dictionary
        event = {
            "eventId": generate_uuid_if_blank(event_id_entry.get()),
            "dpaId": generate_uuid_if_blank(dpa_id_entry.get()),
            "dpaName": dpa_name_combobox.get(),
            "channels": [ch.strip() for ch in channels_entry.get().split(",") if ch.strip()],
            "dateTimeStart": start_datetime,
            "dateTimeEnd": end_datetime,
        }
        if recurrence_entry.get().strip():
            event["recurrence"] = recurrence_entry.get().strip()

        if not validate_datetime(start_datetime) or not validate_datetime(end_datetime):
            raise ValueError("Start/End must be valid ISO 8601 format.")

        # Load schema
        schema_path = os.path.join(os.path.dirname(__file__), "tardys3_schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        dpa_names = schema["definitions"]["ScheduledEvent"]["properties"]["dpaName"]["enum"]

        # Load or initialize JSON file
        json_path = os.path.join(os.getcwd(), "tardys3.json")
        try:
            with open(json_path) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                "transactionId": "",
                "dateTimePublished": "",
                "dateTimeCreated": "",
                "checksum": "",
                "scheduledEvents": []
            }
        except JSONDecodeError:
            raise ValueError("The JSON file is corrupt or improperly formatted.")

        # Fill top-level fields
        data["transactionId"] = generate_uuid_if_blank(transaction_id_entry.get())
        data["dateTimePublished"] = published_date_entry.get()
        data["dateTimeCreated"] = created_date_entry.get()
        data["checksum"] = checksum_entry.get()

        # Append event
        data.setdefault("scheduledEvents", []).append(event)

        # Validate
        validate(instance=data, schema=schema)

        # Save
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Success", "TARDyS3 reservation saved successfully!")

    except ValidationError as ve:
        messagebox.showerror("Schema Validation Error", str(ve))
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"{type(e).__name__}: {e}")

def main():
    global transaction_id_entry, published_date_entry, created_date_entry, checksum_entry
    global event_id_entry, dpa_id_entry, dpa_name_combobox, channels_entry
    global start_date_entry, start_time_combo, end_date_entry, end_time_combo, recurrence_entry

    root = tk.Tk()
    root.title("TARDyS3 Reservation Generator")

    # Layout
    labels = [
        "Transaction ID (blank = auto)",
        "Date Published (yyyy-mm-dd)",
        "Date Created (yyyy-mm-dd)",
        "Checksum",
        "Event ID (blank = auto)",
        "DPA ID (blank = auto)",
        "DPA Name",
        "Channels (comma-separated UUIDs)",
        "Start Date",
        "Start Time",
        "End Date",
        "End Time",
        "Recurrence (optional)"
    ]

    # Fields
    row = 0
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    transaction_id_entry = tk.Entry(root, width=40)
    transaction_id_entry.grid(row=row, column=1)

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    published_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    published_date_entry.grid(row=row, column=1)

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    created_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    created_date_entry.grid(row=row, column=1)

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    checksum_entry = tk.Entry(root, width=40)
    checksum_entry.grid(row=row, column=1)

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    event_id_entry = tk.Entry(root, width=40)
    event_id_entry.grid(row=row, column=1)

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    dpa_id_entry = tk.Entry(root, width=40)
    dpa_id_entry.grid(row=row, column=1)

    # Load schema early for dpa_names
    schema_path = os.path.join(os.path.dirname(__file__), "tardys3_schema.json")
    with open(schema_path) as f:
        schema = json.load(f)
    dpa_names = schema["definitions"]["ScheduledEvent"]["properties"]["dpaName"]["enum"]

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    dpa_name_combobox = ttk.Combobox(root, values=dpa_names, width=37, state="readonly")
    dpa_name_combobox.grid(row=row, column=1)
    dpa_name_combobox.set(dpa_names[0])  # Default to first

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    channels_entry = tk.Entry(root, width=40)
    channels_entry.grid(row=row, column=1)

    # Start date/time
    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    start_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    start_date_entry.grid(row=row, column=1)

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    times = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
    start_time_combo = ttk.Combobox(root, values=times, width=37, state="readonly")
    start_time_combo.grid(row=row, column=1)
    start_time_combo.set("00:00")

    # End date/time
    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    end_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    end_date_entry.grid(row=row, column=1)

    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    end_time_combo = ttk.Combobox(root, values=times, width=37, state="readonly")
    end_time_combo.grid(row=row, column=1)
    end_time_combo.set("00:30")

    # Recurrence
    row += 1
    tk.Label(root, text=labels[row]).grid(row=row, column=0, sticky='e')
    recurrence_entry = tk.Entry(root, width=40)
    recurrence_entry.grid(row=row, column=1)

    # Submit
    row += 1
    tk.Button(root, text="Submit", command=submit).grid(row=row, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
