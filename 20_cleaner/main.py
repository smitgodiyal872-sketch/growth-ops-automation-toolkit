import pandas as pd
import re
import os

# --- PART 1: GENERATE DUMMY DATA (For Testing) ---
# We create a messy file to simulate a bad export from a tool
def create_messy_file(filename="messy_leads.csv"):
    data = {
        "Full Name": ["john doe", "SARAH SMITH", "Mike O'Neil", "john doe", "  Ebony Dark'ness "],
        "Email Address": ["john@gmail.com", "sarah.smith@company.co", "mike.oneil@", "john@gmail.com", "ebony@vampire.net"],
        "Phone": ["123-456-7890", "N/A", "555.123.4567", "123-456-7890", "unknown"]
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"⚠️  Created '{filename}' with messy data for testing.\n")

# --- PART 2: THE CLEANING LOGIC ---

def clean_leads(input_file, output_file):
    print(f"🧹 Starting cleanup on {input_file}...")
    
    # 1. Load the Data
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: File not found!")
        return

    # 2. Standardization (Title Casing Names)
    # Converts "john doe" -> "John Doe" and "SARAH SMITH" -> "Sarah Smith"
    if "Full Name" in df.columns:
        df["Full Name"] = df["Full Name"].str.strip().str.title()
        print("✅ Names standardized to Title Case.")

    # 3. Deduplication
    # Removes rows where the Email Address is exactly the same
    initial_count = len(df)
    if "Email Address" in df.columns:
        df.drop_duplicates(subset=["Email Address"], keep="first", inplace=True)
        print(f"✅ Removed {initial_count - len(df)} duplicate rows.")

    # 4. Email Validation (Regex)
    # Basic check: Must have characters + @ + characters + . + characters
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, str(email)) is not None

    if "Email Address" in df.columns:
        # Create a separate file for bad emails (optional but good practice)
        bad_emails = df[~df["Email Address"].apply(is_valid_email)]
        if not bad_emails.empty:
            print(f"⚠️  Found {len(bad_emails)} invalid emails. Removing them...")
            df = df[df["Email Address"].apply(is_valid_email)]

    # 5. Export
    df.to_csv(output_file, index=False)
    print(f"\n✨ Success! Clean data saved to: {output_file}")
    print(f"📊 Final Lead Count: {len(df)}")

# --- EXECUTION ---
if __name__ == "__main__":
    # Create the test file first
    create_messy_file()
    
    # Run the cleaner
    clean_leads("messy_leads.csv", "clean_crm_ready.csv")
