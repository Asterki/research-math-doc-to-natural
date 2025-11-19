from ollama import Client
import time

# Connect to Ollama server
LLM_NAME = "gemma3:12b"
client = Client(host='http://10.252.1.2:11435')
TEMP = 0.1  # Low temperature for deterministic output

def format_for_prompt(chunk):
    """Prepare the content of the user message."""
    symbols_text = "\n".join(chunk)
    return (
        "You are a LaTeX translator. Your task is to convert LaTeX symbols into plain English descriptions. "
        "Do NOT add any explanation, commentary, or extra text—only translate the symbols. "
        "These symbols are part of a broader document, so maintain continuity and do not alter the meaning. "
        "Return the result as a JSON object mapping symbols to English descriptions, "
        "WITHOUT surrounding curly braces at the very start or end. "
        "Use double quotes for all strings.\n\n"
        "Example:\n"
        "\\alpha → \"alpha\"\n"
        "\\sum → \"summation\"\n"
        "\\forall → \"for all\"\n\n"
        f"Now translate the following symbols:\n{symbols_text}"
    )

def process_chunk(chunk):
    user_message = format_for_prompt(chunk)
    response = client.chat(
        model=LLM_NAME,
        messages=[
            {"role": "system", "content": "You are a LaTeX translator."},
            {"role": "user", "content": user_message}
        ],
        options={"temperature":0.1}
    )
    print(response.message.content)
    # Depending on Ollama version, the text might be in response['response'] or response.text
    text_output = response.get("response") or getattr(response, "text", "")
    return text_output.strip()

def latex_to_natural(latex_list, chunk_size=500):
    englishified_list = []
    for i in range(0, len(latex_list), chunk_size):
        chunk = latex_list[i:i + chunk_size]
        print(f"Processing chunk {i // chunk_size + 1} ({len(chunk)} symbols)...")
        try:
            englishified = process_chunk(chunk)
            print(englishified)
            englishified_list.append(englishified)
        except Exception as e:
            print(f"Error processing chunk {i // chunk_size + 1}: {e}")
            time.sleep(5)  # retry delay
    return englishified_list
