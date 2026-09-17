import os
import pandas as pd
from extractor import ReceiptExtractor
from sample_data import MOCK_RECEIPTS


def run_tier1_pipeline():
    print("==================================================")
    print("    RUNNING TIER 1 MOCK EXTRACTION PIPELINE       ")
    print("==================================================\n")

    extractor = ReceiptExtractor()
    extracted_records = []

    for key, receipt_text in MOCK_RECEIPTS.items():
        print(f"--> Processing Mock Receipt Key: [{key.upper()}]...")
        try:
            parsed = extractor.extract(receipt_text)
            
            # Convert Pydantic object into flat dictionary for Pandas tabular logging
            record = {
                "mock_key": key,
                "merchant_name": parsed.merchant_name,
                "transaction_date": str(parsed.transaction_date),
                "subtotal": parsed.subtotal,
                "tax_amount": parsed.tax_amount,
                "tip_amount": parsed.tip_amount,
                "total_amount": parsed.total_amount,
                "currency": parsed.currency,
                "item_count": len(parsed.line_items),
                "items_summary": ", ".join([item.description for item in parsed.line_items]),
            }
            extracted_records.append(record)
            print(f"    ✓ Extracted {parsed.merchant_name} | {parsed.currency} {parsed.total_amount}")
        except Exception as e:
            print(f"    ❌ Extraction Failed for [{key}]: {e}")

    # Build Pandas DataFrame
    df = pd.DataFrame(extracted_records)
    
    # Save output to disk
    os.makedirs("output", exist_ok=True)
    output_path = "output/tier1_extracted_receipts.csv"
    df.to_csv(output_path, index=False)
    
    print("\n==================================================")
    print("                PIPELINE SUMMARY                  ")
    print("==================================================")
    print(df[["mock_key", "merchant_name", "transaction_date", "total_amount", "currency"]])
    print(f"\nSaved clean audit CSV to: {output_path}\n")


if __name__ == "__main__":
    run_tier1_pipeline()