from flask import Flask, render_template, request, send_file
import pandas as pd
from fpdf import FPDF
import os

app = Flask(__name__)

# Load data from the Excel file into a DataFrame
data = pd.read_excel('database.xlsx')

# Clean column names to avoid KeyErrors
data.columns = data.columns.str.strip()  # Strip whitespace from column names

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the search parameters from the form
        name = request.form.get('name', '')
        state = request.form.get('state', '')
        postal_code = request.form.get('postal_code', '')
        service_category = request.form.get('service_category', '')

        # Filter the data based on the search criteria
        filtered_data = data.copy()

        if 'Name' in filtered_data.columns:
            if name:
                filtered_data = filtered_data[filtered_data['Name'].str.contains(name, na=False, case=False)]
        if 'State' in filtered_data.columns:
            if state:
                filtered_data = filtered_data[filtered_data['State'].str.contains(state, na=False, case=False)]
        if 'Postal Code' in filtered_data.columns:
            if postal_code:
                filtered_data = filtered_data[filtered_data['Postal Code'].astype(str).str.contains(postal_code, na=False)]
        if 'Service Category' in filtered_data.columns:
            if service_category:
                filtered_data = filtered_data[filtered_data['Service Category'].str.contains(service_category, na=False, case=False)]

        return render_template('index.html', data=filtered_data)

    # Display first 10 rows by default
    return render_template('index.html', data=data.head(10))

@app.route('/search', methods=['POST'])
def search():
    name = request.form.get('name', '')
    state = request.form.get('state', '')
    postal_code = request.form.get('postal_code', '')
    service_category = request.form.get('service_category', '')

    results = data.copy()

    # Check for column existence and filter the results
    if 'Name' in results.columns:
        if name:
            results = results[results['Name'].str.contains(name, case=False, na=False)]
    if 'State' in results.columns:
        if state:
            results = results[results['State'].str.contains(state, case=False, na=False)]
    if 'Postal Code' in results.columns:
        if postal_code:
            results = results[results['Postal Code'].astype(str).str.contains(postal_code, na=False)]
    if 'Service Category' in results.columns:
        if service_category:
            results = results[results['Service Category'].str.contains(service_category, case=False, na=False)]

    return render_template('index.html', data=results)

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    name = request.form.get('name', '')
    state = request.form.get('state', '')
    postal_code = request.form.get('postal_code', '')
    service_category = request.form.get('service_category', '')

    results = data.copy()

    # Check for column existence and filter the results
    if 'Name' in results.columns:
        if name:
            results = results[results['Name'].str.contains(name, case=False, na=False)]
    if 'State' in results.columns:
        if state:
            results = results[results['State'].str.contains(state, case=False, na=False)]
    if 'Postal Code' in results.columns:
        if postal_code:
            results = results[results['Postal_Code'].astype(str).str.contains(postal_code, na=False)]
    if 'Service Category' in results.columns:
        if service_category:
            results = results[results['Service_Category'].str.contains(service_category, case=False, na=False)]

    # Create PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Community Database Results", ln=True, align='C')
    pdf.ln(10)

    # Add headers
    pdf.cell(30, 10, "Name", border=1)
    pdf.cell(40, 10, "Contact", border=1)
    pdf.cell(70, 10, "Details", border=1)
    pdf.cell(30, 10, "State", border=1)
    pdf.cell(30, 10, "Postal_Code", border=1)
    pdf.cell(50, 10, "Service_Category", border=1)
    pdf.ln()

    # Add results
    for index, row in results.iterrows():
        pdf.cell(30, 10, str(row['Name']), border=1)
        pdf.cell(40, 10, str(row['Contact']), border=1)
        pdf.cell(70, 10, str(row['Details']), border=1)
        pdf.cell(30, 10, str(row['State']), border=1)
        pdf.cell(30, 10, str(row['Postal_Code']), border=1)
        pdf.cell(50, 10, str(row['Service_Category']), border=1)
        pdf.ln()

    pdf_file_path = 'results.pdf'
    pdf.output(pdf_file_path)

    return send_file(pdf_file_path, as_attachment=True)

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
