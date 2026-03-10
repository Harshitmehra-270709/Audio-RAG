import os
import json

TRANSCRIPT_FOLDER = "transcript"
OUTPUT_FOLDER = "chunks"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file_name in os.listdir(TRANSCRIPT_FOLDER):

    if file_name.endswith(".json"):

        input_path = os.path.join(TRANSCRIPT_FOLDER, file_name)

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chunks = []
        current_text = ""
        chunk_start = None
        chunk_id = 0

        for seg in data:

            if chunk_start is None:
                chunk_start = seg["start"]

            current_text += " " + seg["text"]

            if seg["end"] - chunk_start >= 45:

                chunks.append({
                    "chunk_id": chunk_id,
                    "text": current_text.strip(),
                    "start": chunk_start,
                    "end": seg["end"],
                    "source": file_name
                })

                chunk_id += 1
                current_text = ""
                chunk_start = None

        if current_text:

            chunks.append({
                "chunk_id": chunk_id,
                "text": current_text.strip(),
                "start": chunk_start,
                "end": data[-1]["end"],
                "source": file_name
            })

        output_name = file_name.replace(".json", "_chunks.json")
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=4)

        print(f"Saved: {output_path}")

print(" All the chunks are created ")