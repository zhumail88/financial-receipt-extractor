import os
import json
from dotenv import load_dotenv
from groq import Groq
from schema import ReceiptData

# Load environment variables from .env file
load_dotenv()


class ReceiptExtractor:
    """Handles receipt text extraction using Groq API and Pydantic validation."""

    def __init__(self, model_name: str = None):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not set or valid. Please set it in your .env file."
            )
        self.client = Groq(api_key=api_key)
        
        # Dynamically set active model if not specified
        if model_name:
            self.model_name = model_name
        else:
            self.model_name = self._get_active_model()

    def _get_active_model(self) -> str:
        """Fetch active model list from Groq API and pick an available model."""
        try:
            models_page = self.client.models.list()
            active_ids = [m.id for m in models_page.data]
            print(f"DEBUG - Active Groq Models found: {active_ids}")
            
            preferred_models = [
                "openai/gpt-oss-20b",
                "openai/gpt-oss-120b",
                "qwen/qwen3.8-27b",
                "groq/compound",
            ]
            for pref in preferred_models:
                if pref in active_ids:
                    print(f"Selected Model: {pref}")
                    return pref
            
            selected = active_ids[0]
            print(f"Selected Fallback Model: {selected}")
            return selected
        except Exception as e:
            print(f"Warning: Could not list models dynamically ({e}). Defaulting to openai/gpt-oss-20b.")
            return "openai/gpt-oss-20b"

    def extract(self, receipt_text: str) -> ReceiptData:
        """
        Sends raw receipt text to Groq API and parses the response into a ReceiptData object.
        """
        schema_json = json.dumps(ReceiptData.model_json_schema(), indent=2)

        system_prompt = (
            "You are an expert AI financial document processor.\n"
            "Your task is to extract structured receipt data from noisy OCR text.\n"
            "You MUST conform strictly to the following JSON Schema:\n"
            f"{schema_json}\n\n"
            "Rules:\n"
            "1. Output ONLY valid JSON matching the schema format.\n"
            "2. Map terms like 'GRAND TOTAL', 'TOTAL DUE', or 'TOTAL PAYABLE' to the 'total_amount' field.\n"
            "3. Infer currency (e.g. PKR, USD, EUR, GBP) from symbols/text, defaulting to 'PKR' if ambiguous.\n"
            "4. Format transaction_date strictly as YYYY-MM-DD. Convert DD/MM/YYYY or YY/MM/DD formats.\n"
            "5. Strip commas from monetary strings before inserting numbers (e.g., '5,337.00' -> 5337.00).\n"
            "6. Do not include markdown headers or commentary outside the JSON."
        )

        user_prompt = f"Extract all financial data from this raw receipt text:\n\n{receipt_text}"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=1024,  # Increased token allowance to complete larger JSON outputs safely
        )

        raw_json_str = response.choices[0].message.content

        parsed_receipt = ReceiptData.model_validate_json(raw_json_str)
        return parsed_receipt


if __name__ == "__main__":
    from sample_data import MOCK_RECEIPT_SIMPLE

    print("Testing Extractor with Tier 1 Simple Mock Receipt...")
    extractor = ReceiptExtractor()
    result = extractor.extract(MOCK_RECEIPT_SIMPLE)
    
    print("\n--- Extracted Receipt Object ---")
    print(f"Merchant: {result.merchant_name}")
    print(f"Date:     {result.transaction_date}")
    print(f"Currency: {result.currency}")
    print(f"Total:    {result.currency} {result.total_amount}")
    print(f"Items Count: {len(result.line_items)}")