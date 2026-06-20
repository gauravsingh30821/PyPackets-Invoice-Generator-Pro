# 📄 PyPackets Invoice Generator Pro

A modern desktop invoice generator built with Python and CustomTkinter.

PyPackets Invoice Generator Pro helps freelancers, developers, agencies, and small businesses create professional PDF invoices quickly and efficiently.

---

## ✨ Features

* Modern CustomTkinter GUI
* Automatic Invoice Number Generation
* Company & Client Information Management
* Service Description Support
* GST/Tax Calculation
* PDF Invoice Export
* Company Logo Upload
* Invoice Notes Section
* Invoice History Tracking
* Client Database Storage
* Revenue Statistics Dashboard
* Dark / Light Theme Toggle
* Single-File Python Application

---

## 🖼 Screenshot

InvoiceFlow provides a clean and professional interface designed for daily invoicing tasks.

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/invoiceflow.git
cd invoiceflow
```

### Install Dependencies

```bash
pip install customtkinter reportlab pillow
```

---

## ▶ Running the Application

```bash
python "PyPackets Invoice Generator Pro.py"
```

---

## 📦 Building EXE

Install PyInstaller:

```bash
pip install pyinstaller
```

Build executable:

```bash
pyinstaller --onefile --windowed --icon=logo.ico "PyPackets Invoice Generator Pro.py"
```

The generated executable will be available in:

```text
dist/
```

---

## 📁 Generated Files

The application automatically creates:

### stats.json

Stores:

* Total invoices generated
* Total revenue earned
* Total clients

### invoice_history.json

Stores invoice history records.

### clients.csv

Stores client database information.

### Generated PDF Files

Every invoice is exported as a professional PDF document.

---

## 🛠 Technologies Used

* Python 3
* CustomTkinter
* ReportLab
* JSON
* CSV

---

## 📊 Dashboard

The dashboard displays:

* Total Revenue
* Total Clients
* Total Invoices Generated

---

## 🔒 Data Storage

All data is stored locally on the user's computer.

No internet connection is required.

No cloud services are used.

---

## 🎯 Future Plans

* Email Invoice Sending
* Multiple Invoice Templates
* Company Profile Manager
* Invoice Search
* Invoice Editing
* Excel Export
* Client Management System
* Multi-Currency Support
* Cloud Backup

---

## 👨‍💻 Developer

PyPackets

Building useful Python tools, utilities, and desktop applications.

---

## 📜 License

MIT License

Feel free to use, modify, and distribute this project.
