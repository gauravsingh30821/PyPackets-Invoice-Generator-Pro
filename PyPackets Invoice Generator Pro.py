import customtkinter as ctk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from datetime import datetime
import json
import csv
import os
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class InvoiceFlow:
    def __init__(self, root):
        self.root = root
        self.root.title("InvoiceFlow - PyPackets")
        self.root.geometry("900x750")

        self.logo_path = ""

        self.create_files()
        self.build_ui()
        self.load_stats()

    def create_files(self):
        if not os.path.exists("stats.json"):
            with open("stats.json", "w") as f:
                json.dump({
                    "invoices": 0,
                    "revenue": 0,
                    "clients": 0
                }, f)

        if not os.path.exists("invoice_history.json"):
            with open("invoice_history.json", "w") as f:
                json.dump([], f)

        if not os.path.exists("clients.csv"):
            with open("clients.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Client"])

    def build_ui(self):

        title = ctk.CTkLabel(
            self.root,
            text="InvoiceFlow",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=10)

        self.theme_btn = ctk.CTkButton(
            self.root,
            text="Toggle Theme",
            command=self.toggle_theme
        )
        self.theme_btn.pack(pady=5)

        self.stats_frame = ctk.CTkFrame(self.root)
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="Loading Stats..."
        )
        self.stats_label.pack(pady=10)

        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            width=850,
            height=500
        )
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.company_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Company Name"
        )
        self.company_entry.pack(fill="x", pady=5)

        self.client_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Client Name"
        )
        self.client_entry.pack(fill="x", pady=5)

        invoice_number = f"INV-{random.randint(1000,9999)}"

        self.invoice_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Invoice Number"
        )
        self.invoice_entry.pack(fill="x", pady=5)
        self.invoice_entry.insert(0, invoice_number)

        self.service_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Service Description"
        )
        self.service_entry.pack(fill="x", pady=5)

        self.amount_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Amount"
        )
        self.amount_entry.pack(fill="x", pady=5)

        self.gst_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="GST Percentage"
        )
        self.gst_entry.pack(fill="x", pady=5)

        notes_label = ctk.CTkLabel(
            self.main_frame,
            text="Invoice Notes"
        )
        notes_label.pack(anchor="w", pady=(10, 0))

        self.notes_box = ctk.CTkTextbox(
            self.main_frame,
            height=120
        )
        self.notes_box.pack(fill="x", pady=5)

        self.logo_btn = ctk.CTkButton(
            self.main_frame,
            text="Upload Company Logo",
            command=self.select_logo
        )
        self.logo_btn.pack(pady=10)

        self.generate_btn = ctk.CTkButton(
            self.main_frame,
            text="Generate PDF Invoice",
            height=40,
            command=self.generate_invoice
        )
        self.generate_btn.pack(fill="x", pady=10)

        self.history_box = ctk.CTkTextbox(
            self.main_frame,
            height=180
        )
        self.history_box.pack(fill="both", pady=10)

        self.load_history()

    def toggle_theme(self):
        current = ctk.get_appearance_mode()

        if current == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def select_logo(self):
        file = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if file:
            self.logo_path = file
            messagebox.showinfo(
                "Logo Selected",
                os.path.basename(file)
            )
    def load_stats(self):
        try:
            with open("stats.json", "r") as f:
                stats = json.load(f)

            self.stats_label.configure(
                text=(
                    f"Invoices: {stats['invoices']}   |   "
                    f"Revenue: ₹{stats['revenue']:.2f}   |   "
                    f"Clients: {stats['clients']}"
                )
            )
        except:
            self.stats_label.configure(text="Stats unavailable")

    def save_client(self, client_name):
        existing = []

        try:
            with open("clients.csv", "r") as f:
                reader = csv.reader(f)

                for row in reader:
                    if row:
                        existing.append(row[0].strip().lower())
        except:
            pass

        if client_name.strip().lower() not in existing:

            with open("clients.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([client_name])

            try:
                with open("stats.json", "r") as f:
                    stats = json.load(f)

                stats["clients"] += 1

                with open("stats.json", "w") as f:
                    json.dump(stats, f, indent=4)

            except:
                pass

    def add_invoice_history(
        self,
        invoice_no,
        client,
        service,
        total
    ):

        try:
            with open("invoice_history.json", "r") as f:
                history = json.load(f)

        except:
            history = []

        history.append(
            {
                "invoice": invoice_no,
                "client": client,
                "service": service,
                "total": total,
                "date": datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )
            }
        )

        with open("invoice_history.json", "w") as f:
            json.dump(history, f, indent=4)

    def load_history(self):

        self.history_box.delete("1.0", "end")

        try:
            with open("invoice_history.json", "r") as f:
                history = json.load(f)

            if not history:
                self.history_box.insert(
                    "end",
                    "No invoices generated yet."
                )
                return

            for item in reversed(history[-20:]):

                line = (
                    f"{item['invoice']} | "
                    f"{item['client']} | "
                    f"₹{item['total']:.2f} | "
                    f"{item['date']}\n"
                )

                self.history_box.insert("end", line)

        except:
            self.history_box.insert(
                "end",
                "Unable to load history."
            )

    def update_stats(self, total_amount):

        try:
            with open("stats.json", "r") as f:
                stats = json.load(f)

            stats["invoices"] += 1
            stats["revenue"] += total_amount

            with open("stats.json", "w") as f:
                json.dump(stats, f, indent=4)

        except:
            pass

        self.load_stats()

    def generate_invoice(self):

        company = self.company_entry.get().strip()
        client = self.client_entry.get().strip()
        invoice_no = self.invoice_entry.get().strip()
        service = self.service_entry.get().strip()

        if not company:
            messagebox.showerror(
                "Error",
                "Company name required."
            )
            return

        if not client:
            messagebox.showerror(
                "Error",
                "Client name required."
            )
            return

        try:
            amount = float(
                self.amount_entry.get()
            )

        except:
            messagebox.showerror(
                "Error",
                "Invalid amount."
            )
            return

        try:
            gst_percent = float(
                self.gst_entry.get()
            )

        except:
            gst_percent = 0

        gst_amount = amount * gst_percent / 100
        total = amount + gst_amount

        notes = self.notes_box.get(
            "1.0",
            "end"
        ).strip()

        preview = (
            f"Invoice: {invoice_no}\n\n"
            f"Client: {client}\n"
            f"Service: {service}\n\n"
            f"Amount: ₹{amount:.2f}\n"
            f"GST: ₹{gst_amount:.2f}\n"
            f"Total: ₹{total:.2f}"
        )

        confirm = messagebox.askyesno(
            "Invoice Preview",
            preview + "\n\nGenerate PDF?"
        )

        if not confirm:
            return
        filename = f"{invoice_no}.pdf"

        pdf = canvas.Canvas(filename)

        if self.logo_path:
            try:
                pdf.drawImage(
                    self.logo_path,
                    420,
                    740,
                    width=120,
                    height=60,
                    preserveAspectRatio=True
                )
            except:
                pass

        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawString(50, 800, "INVOICE")

        pdf.setFont("Helvetica", 12)

        current_date = datetime.now().strftime(
            "%d-%m-%Y"
        )

        pdf.drawString(
            50,
            770,
            f"Date: {current_date}"
        )

        pdf.drawString(
            50,
            745,
            f"Invoice No: {invoice_no}"
        )

        pdf.drawString(
            50,
            700,
            f"Company: {company}"
        )

        pdf.drawString(
            50,
            675,
            f"Client: {client}"
        )

        pdf.line(50, 650, 550, 650)

        pdf.setFont(
            "Helvetica-Bold",
            13
        )

        pdf.drawString(
            50,
            620,
            "Service Description"
        )

        pdf.drawString(
            400,
            620,
            "Amount"
        )

        pdf.line(
            50,
            610,
            550,
            610
        )

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawString(
            50,
            580,
            service
        )

        pdf.drawString(
            400,
            580,
            f"₹{amount:.2f}"
        )

        pdf.line(
            50,
            540,
            550,
            540
        )

        pdf.drawString(
            350,
            510,
            "GST:"
        )

        pdf.drawString(
            450,
            510,
            f"₹{gst_amount:.2f}"
        )

        pdf.drawString(
            350,
            480,
            "TOTAL:"
        )

        pdf.drawString(
            450,
            480,
            f"₹{total:.2f}"
        )

        pdf.line(
            340,
            470,
            540,
            470
        )

        pdf.setFont(
            "Helvetica-Bold",
            14
        )

        pdf.drawString(
            50,
            420,
            "Notes"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        y = 395

        for line in notes.split("\n"):
            pdf.drawString(
                50,
                y,
                line[:90]
            )
            y -= 18

            if y < 100:
                break

        pdf.line(
            50,
            90,
            550,
            90
        )

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawString(
            50,
            70,
            "Generated using InvoiceFlow by PyPackets"
        )

        pdf.save()

        self.save_client(client)

        self.update_stats(total)

        self.add_invoice_history(
            invoice_no,
            client,
            service,
            total
        )

        self.load_history()

        self.invoice_entry.delete(0, "end")
        self.invoice_entry.insert(
            0,
            f"INV-{random.randint(1000,9999)}"
        )

        self.client_entry.delete(0, "end")
        self.service_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.gst_entry.delete(0, "end")
        self.notes_box.delete(
            "1.0",
            "end"
        )

        messagebox.showinfo(
            "Success",
            f"Invoice saved as\n{filename}"
        )


if __name__ == "__main__":

    root = ctk.CTk()

    app = InvoiceFlow(root)

    root.mainloop()
