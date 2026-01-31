
try:
    from src.multilingual.translator import ContractTranslator
    print("Import successful")
    translator = ContractTranslator()
    text = "नमस्ते दुनिया"
    translated = translator.translate_to_english(text)
    print(f"Translation: {translated}")
except Exception as e:
    print(f"Error: {e}")
