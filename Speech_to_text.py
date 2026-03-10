from faster_whisper import WhisperModel
import os 
import json
DATA_FOLDER ="data"
OUTPUT_FOLDER = "transcript"
MODLE_SIZE= "large-v2"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = WhisperModel(
    MODLE_SIZE,
    device="cuda",
    compute_type="float16"
)

def transcribe_to_english(audio_path):
    segments,info =model.transcribe(
        audio_path,
        task="translate"
    )
    transcript_data=[]
    for segment in segments:
        transcript_data.append(
            {
            "text": segment.text.strip(),
            "start": round(segment.start , 2),
            "end" : round(segment.end ,2)

        })
    return transcript_data
for file_name in os.listdir(DATA_FOLDER):
    if(file_name.endswith(".mp3")):
        file_path = os.path.join(DATA_FOLDER, file_name)
        print(f"\nProcessing: {file_name}")

        transcript = transcribe_to_english(file_path)

        output_file = os.path.splitext(file_name)[0] + ".json"
        output_path = os.path.join(OUTPUT_FOLDER, output_file)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcript, f, indent=4, ensure_ascii=False)

        print(f"Saved → {output_path}")
print("the task is completed")

