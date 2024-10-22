import os
import PyPDF2
from datetime import datetime
import csv
import re
from collections import defaultdict

def extract_date_and_earnings(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = reader.pages[0].extract_text()
            print(f"\nProcessing {pdf_path}")
            print("Extracted text:", text[:200] + "...")  # Print first 200 chars for debugging
            
            # Extract date
            date_match = re.search(r'Check Date:(\d{2}/\d{2}/\d{4})', text)
            if not date_match:
                print(f"No date found in {pdf_path}")
                # Try alternate date format
                date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
                if not date_match:
                    return None, None
            
            date_str = date_match.group(1)
            date = datetime.strptime(date_str, '%m/%d/%Y')
            print(f"Found date: {date_str}")
            
            # Extract earnings - try multiple patterns
            earnings = 0
            
            # Try to find salary in EARNINGS section
            earnings_section = re.search(r'EARNINGS.*?Total.*?\$([\d,]+\.\d{2})', text, re.DOTALL)
            if earnings_section:
                earnings = float(earnings_section.group(1).replace(',', ''))
                print(f"Found earnings: ${earnings}")
            else:
                # Try to find individual salary line
                salary_match = re.search(r'Salary.*?\$([\d,]+\.\d{2})', text)
                if salary_match:
                    salary = float(salary_match.group(1).replace(',', ''))
                    print(f"Found salary: ${salary}")
                    
                    # Add GTL if present
                    gtl_match = re.search(r'GTL.*?\$([\d,]+\.\d{2})', text)
                    if gtl_match:
                        gtl = float(gtl_match.group(1).replace(',', ''))
                        print(f"Found GTL: ${gtl}")
                        earnings = salary + gtl
                    else:
                        earnings = salary
            
            if earnings == 0:
                print("Warning: No earnings found")
                return None, None
                
            print(f"Total earnings: ${earnings:.2f}")
            return date, earnings
            
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return None, None

def get_quarter(date):
    return (date.year, (date.month - 1) // 3 + 1)

def quarter_to_date_range(year, quarter):
    quarters = {
        1: ('01/01', '03/31'),
        2: ('04/01', '06/30'),
        3: ('07/01', '09/30'),
        4: ('10/01', '12/31')
    }
    start, end = quarters[quarter]
    return f"{start}", f"{end}"

# Process all PDFs
pdf_directory = "PDFS"
data = []

print("\nStarting PDF processing...")
for filename in sorted(os.listdir(pdf_directory)):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        date, earnings = extract_date_and_earnings(pdf_path)
        if date and earnings:
            data.append((date, earnings))
            print(f"Successfully processed {filename}: {date.strftime('%m/%d/%Y')} - ${earnings:.2f}")
        else:
            print(f"Failed to extract data from {filename}")

print(f"\nSuccessfully processed {len(data)} PDFs")

# Sort data by date
data.sort(key=lambda x: x[0])

# Group by quarters
quarterly_totals = defaultdict(float)
for date, earnings in data:
    quarter_key = get_quarter(date)
    quarterly_totals[quarter_key] += earnings

print("\nQuarterly totals:")
for (year, quarter), total in sorted(quarterly_totals.items()):
    print(f"Q{quarter} {year}: ${total:.2f}")

# Save to CSV
csv_path = 'CSVDATA/earnings.csv'
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Quarter', 'Start Date', 'End Date', 'Gross Earnings'])
    
    for (year, quarter), total in sorted(quarterly_totals.items()):
        start_date, end_date = quarter_to_date_range(year, quarter)
        writer.writerow([f"Q{quarter} {year}", start_date, end_date, f"${total:.2f}"])

print(f"\nSaved results to {csv_path}")

# Answer questions
def format_quarter(year, quarter):
    start_date, end_date = quarter_to_date_range(year, quarter)
    return f"Gross wages earned from {start_date}/{year} to {end_date}/{year}: ${quarterly_totals.get((year, quarter), 0):.2f}"

answers = [
    format_quarter(2024, 4),  # 10/01/2024 to 12/31/2024
    format_quarter(2024, 3),  # 07/01/2024 to 09/30/2024
    format_quarter(2024, 2),  # 04/01/2024 to 06/30/2024
    format_quarter(2024, 1),  # 01/01/2024 to 03/31/2024
    format_quarter(2023, 4),  # 10/01/2023 to 12/31/2023
    format_quarter(2023, 3),  # 07/01/2023 to 09/30/2023
]

# Write answers to a file
with open('answers.txt', 'w') as f:
    for answer in answers:
        f.write(answer + '\n')

print("\nAnswers written to answers.txt")
