
# PDF Password Cracker

## Overview
This Python script attempts to crack the password of an encrypted PDF file using a brute-force approach. It systematically tries numeric passwords, starting with single-digit passwords (0-9) and progressing to passwords up to 8 digits long (0-99999999). The script leverages multiprocessing to speed up the cracking process by distributing the workload across multiple CPU cores.

## Features
- Checks if the PDF is encrypted before attempting to crack it.
- Starts with quick single-digit password attempts (0-9).
- Uses multiprocessing for passwords of lengths 2 to 8.
- Provides progress updates during the cracking process.
- Outputs the found password and time taken, or notifies if no password is found up to 8 digits.

## Requirements
- Python 3.x
- Required Python libraries:
  - `PyPDF2` (install via `pip install PyPDF2`)
- A PDF file that is password-protected with a numeric password.

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install the required library:
   ```bash
   pip install PyPDF2
   ```
3. Save the script as `pdf_cracker.py` (or any preferred name).

## Usage
1. Place the encrypted PDF file in the same directory as the script (or provide the full file path).
2. Update the `pdf_path` variable in the script to point to your PDF file:
   ```python
   pdf_path = "your_encrypted_file.pdf"
   ```
3. Run the script:
   ```bash
   python pdf_cracker.py
   ```
4. The script will:
   - Check if the PDF is encrypted.
   - Attempt passwords from 0-9, then 00-99999999.
   - Display progress and results in the terminal.

## Example Output
```
ℹ️ Starting password cracking for '1.pdf'...
ℹ️ Checking single-digit passwords (0-9)...
ℹ️ Trying passwords of length 2 (0-99) with 4 processes...
ℹ️ Testing length 2: 0050
🔥 Password found: 0072
⏳ Time taken: 2.34 seconds
```

## Notes
- The script only attempts numeric passwords (e.g., "123", "00004567").
- It stops at 8-digit passwords to avoid excessive runtime; modify the `range(2, 9)` in the script to extend this limit if needed.
- Interrupting the script with `Ctrl+C` will display a graceful exit message.
- Ensure you have legal permission to crack the PDF password, as unauthorized use may violate laws or terms of service.

## Limitations
- Works only with PDFs encrypted with numeric passwords.
- May not succeed if the password includes letters, symbols, or exceeds 8 digits.
- Performance depends on CPU core count and system resources.

## License
This script is provided as-is for educational purposes. Use responsibly.

--- 
