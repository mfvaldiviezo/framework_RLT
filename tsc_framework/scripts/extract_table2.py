import json
from pathlib import Path

transcript_path = Path("C:/Users/mfval/.gemini/antigravity-ide/brain/b16f95eb-4450-43f5-8433-c0b14a727d41/.system_generated/logs/transcript_full.jsonl")
if not transcript_path.exists():
    transcript_path = Path("C:/Users/mfval/.gemini/antigravity-ide/brain/b16f95eb-4450-43f5-8433-c0b14a727d41/.system_generated/logs/transcript.jsonl")

with transcript_path.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "TABLE II" in line or "Table II" in line or "Throughput-performance" in line:
            data = json.loads(line)
            content = data.get("content", "")
            if "\\begin{table" in content and "II" in content:
                print("FOUND TABLE II IN LATEX:")
                lines = content.split("\n")
                start = False
                for l in lines:
                    if "\\begin{table" in l or "TABLE II" in l:
                        start = True
                    if start:
                        print(l)
                        if "\\end{table" in l:
                            break
                break
