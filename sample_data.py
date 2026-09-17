"""
Tier 1 Mock Data: Raw, noisy, OCR-style text strings representing Pakistani receipts.
"""

MOCK_RECEIPT_SIMPLE = """
AL-FATAH ELECTRONICS & GROCERY
MM ALAM ROAD, GULBERG III, LAHORE
DATE: 15/03/2024  TIME: 14:32

1x OLPER'S MILK 1L ...... PKR 290.00
2x TAPAL TEA 450G ....... PKR 1,100.00
1x DAWN BREAD LARGE ..... PKR 210.00

SUBTOTAL: PKR 1,600.00
GST (18%): PKR 288.00
TOTAL AMOUNT: PKR 1,888.00

PAID VIA DEBIT CARD **** 4821
THANK YOU FOR SHOPPING AT AL-FATAH!
"""

MOCK_RECEIPT_MESSY = """
=== MONAL RESTAURANT PIR SOHAWA ===
ISLAMABAD | TEL: 051-2898044
Server: Tariq | Table: 18
Date: 2024-08-01

Chicken Karahi (Full) ..... 2,850.00
Garlic Naan (4x) .......... 480.00
Mint Margarita (2x) ....... 700.00
Gulab Jamun ............... 350.00

Food/Bev Subtotal: 4,380.00
PRA Tax (15%): 657.00
Service Charge: 300.00
GRAND TOTAL: PKR 5,337.00

Payment: VISA CARD
Auth Code: 882910
* Software Powered by RestoTech PK *
"""

MOCK_RECEIPT_AMBIGUOUS = """
KHADI OUTFITS & RETAIL
PACKAGES MALL, LAHORE
DATE: 10/11/23

ITEMS:
COTTON KURTA - PRINTED - 4,990.00
EMBROIDERED DUPATTA - 2,500.00

DISCOUNT APPLIED: -1,000.00
TOTAL PAYABLE: 6,490.00

CURRENCY: PKR
Inclusive of all local taxes.
"""

MOCK_RECEIPTS = {
    "simple": MOCK_RECEIPT_SIMPLE,
    "messy": MOCK_RECEIPT_MESSY,
    "ambiguous": MOCK_RECEIPT_AMBIGUOUS,
}


if __name__ == "__main__":
    print(f"Loaded {len(MOCK_RECEIPTS)} Mock receipts for Tier 1 testing.")