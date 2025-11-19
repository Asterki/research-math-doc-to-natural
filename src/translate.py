from ollama import Client 
import time

# Configuration
LLM_NAME = "gemma3:12b"
CHUNK_SIZE = 500  # Adjust as needed based on line length
INPUT_FILE = "SYMLIST"
OUTPUT_FILE = "latex_symbols_english.txt"

# Connect to your Ollama server (replace with your actual host/port if needed)
client = Client(host='http://10.252.1.2:11435')

def read_chunks(file_path, chunk_size):
    """Yield chunks of lines from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        chunk = []
        for line in f:
            line = line.strip()
            if line:
                chunk.append(line)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

def format_for_prompt(chunk):
    """Prepare prompt for LLM."""
    # Just list the LaTeX symbols, ask for English equivalents
    symbols_text = "\n".join(chunk)
    prompt = ( "Translate the following LaTeX symbols into plain English. Do not add extra explanation to what the symbols are. You are solely translating formulas into plain English. These are part of a borader context, so do not break continuity" "Return a JSON object mapping symbols to English descriptions, " "without surrounding curly braces at the very start or end.\n\n" f"{symbols_text}" )
    return prompt

def process_chunk(chunk):
    prompt = format_for_prompt(chunk)
    response = client.generate(model=LLM_NAME, prompt=prompt)
    print(response["response"])
    return response.text.strip()

def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        for i, chunk in enumerate(read_chunks(INPUT_FILE, CHUNK_SIZE), start=1):
            print(f"Processing chunk {i} ({len(chunk)} symbols)...")
            try:
                englishified = process_chunk(chunk)
                out_file.write(englishified + "\n")
                out_file.flush()
            except Exception as e:
                print(f"Error processing chunk {i}: {e}")
                time.sleep(5)  # retry delay
    print("Processing complete. Results saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
