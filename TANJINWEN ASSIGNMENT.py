import pytesseract
from PIL import Image
import glob
import os
from tabulate import tabulate

def extract_information_from_receipt(image_path):
    # Load the receipt image
    image = Image.open(image_path)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)

    # Find total amount
    total_amount = None
    # Replace 'Total:' with any relevant keyword that indicates the total amount on your receipts
    total_amount_keyword = 'Total:'
    if total_amount_keyword in text:
        start_index = text.index(total_amount_keyword) + len(total_amount_keyword)
        total_amount = text[start_index:].split()[0]

    # Find invoice number
    invoice_number = None
    # Replace 'Invoice:' with any relevant keyword that indicates the invoice number on your receipts
    invoice_number_keyword = 'Invoice No:'
    if invoice_number_keyword in text:
        start_index = text.index(invoice_number_keyword) + len(invoice_number_keyword)
        invoice_number = text[start_index:].split()[0]

    # Find receipt number
    receipt_number = None
    # Replace 'Receipt:' with any relevant keyword that indicates the receipt number on your receipts
    receipt_number_keyword = 'Receipt No:'
    if receipt_number_keyword in text:
        start_index = text.index(receipt_number_keyword) + len(receipt_number_keyword)
        receipt_number = text[start_index:].split()[0]

    # Find date
    date = None
    # Replace 'Date:' with any relevant keyword that indicates the date on your receipts
    date_keyword = 'Date:'
    if date_keyword in text:
        start_index = text.index(date_keyword) + len(date_keyword)
        date = text[start_index:].split()[0]

    # Return the extracted information as a list
    return [total_amount, invoice_number, receipt_number, date]

# Specify the directory containing your receipt images
directory = '/home/jinwentan/Desktop/CIM assignment 1 /Invoice/'

# Create a glob pattern to match PNG files in the directory
file_pattern = os.path.join(directory, '*.png')

# Extract information from the receipt images
receipts_table_data = []
invoices_table_data = []

for image_path in glob.glob(file_pattern):
    extracted_info = extract_information_from_receipt(image_path)
    filename = os.path.basename(image_path)

    # Separate receipts and invoices based on invoice number presence
    if extracted_info[1]:
        invoices_table_data.append([filename] + extracted_info)
    else:
        receipts_table_data.append([filename] + extracted_info)

# Define the table headers
headers = ['Receipt', 'Total Amount', 'Invoice Number', 'Receipt Number', 'Date']
headers = ['Receipt', 'Total Amount', 'Invoice Number', 'Receipt Number', 'Date']

# Print the receipts table
print("Receipts:")
print(tabulate(receipts_table_data, headers=headers, tablefmt='grid'))
print()

# Print the invoices table
print("Invoices:")
print(tabulate(invoices_table_data, headers=headers, tablefmt='grid'))
