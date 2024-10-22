# PDF Pay Stub Processor

This Python script processes PDF pay stubs to extract and analyze quarterly earnings data. It reads multiple PDF pay stubs, extracts the dates and earnings information, calculates quarterly totals, and generates both a CSV report and answers to specific earnings questions.

This was specifically written for getting data from Namely paystubs for answering questions for the california edd application.

## Requirements

- Python 3.x
- PyPDF2 library
- Virtual environment (venv)

## Project Structure

```
.
├── PDFS/               # Directory containing PDF pay stubs
├── CSVDATA/            # Output directory for CSV reports
├── process_pdfs.py     # Main processing script
├── questions.txt       # Input questions file
└── answers.txt         # Generated answers file
```

## Installation

1. Ensure you have Python 3.x installed
2. Set up and activate the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   ```
3. Install required packages:
   ```bash
   pip install PyPDF2
   ```

## Usage

1. Place your PDF pay stubs in the `PDFS` directory
2. Ensure your questions are in `questions.txt`
3. Run the script:
   ```bash
   python process_pdfs.py
   ```

## Output

The script generates two output files:

1. `CSVDATA/earnings.csv`: Contains quarterly earnings data with columns:
   - Quarter
   - Start Date
   - End Date
   - Gross Earnings

2. `answers.txt`: Contains answers to specific quarterly earnings questions

## Features

- Processes multiple PDF pay stubs
- Extracts pay dates and earnings information
- Calculates quarterly totals
- Generates CSV report
- Answers specific earnings questions
- Handles various date formats
- Includes error handling and processing feedback

## Data Processing

The script:
1. Reads each PDF in the PDFS directory
2. Extracts check dates and gross earnings
3. Groups data by quarters
4. Calculates quarterly totals
5. Generates formatted reports

## Error Handling

- Validates PDF content
- Provides processing feedback
- Skips invalid or unreadable files
- Reports processing status for each file
