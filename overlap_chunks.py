import os
import json
import tiktoken

INPUT_FOLDER = "chunks"
OUTPUT_FOLDER = "overlap_chunks"

os.makedirs(OUTPUT_FOLDER , exist_ok=True)

enc = tiktoken.get_encoding("cl100k_base")

def chunk_with_overlap(text , chunk_size=500 , overlap =100):
    tokens = enc.encode(text)

    results =[]
    start = 0

    while(start <len(tokens)):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]

        chunk_text =enc.decode(chunk_tokens)

        results.append(chunk_text)

        start+= chunk_size - overlap
    return results
for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".json"):
        path = os.path.join(INPUT_FOLDER, file)

        with open(path , "r" , encoding="utf-8") as f:
            data = json.load(f)
        
        new_chunks = []
        chunk_id = 0

        for chunk in data:

            overlapped = chunk_with_overlap(chunk["text"])

            for text in overlapped:
                new_chunks.append(
                    {
                        "chunk_id":chunk_id,
                        "text":text,
                        "start":chunk["start"],
                        "end":chunk["end"],
                        "source":chunk["source"]
                    }
                )

                chunk_id+=1

        output_path = os.path.join(OUTPUT_FOLDER, file)
        with open(output_path , "w" , encoding="utf-8") as f:
            json.dump(new_chunks , f, indent=4)
        print(f"saved {output_path}")
