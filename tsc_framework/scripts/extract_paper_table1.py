import json
from pathlib import Path

transcript_path = Path("C:/Users/mfval/.gemini/antigravity-ide/brain/b16f95eb-4450-43f5-8433-c0b14a727d41/.system_generated/logs/transcript_full.jsonl")

if not transcript_path.exists():
    transcript_path = Path("C:/Users/mfval/.gemini/antigravity-ide/brain/b16f95eb-4450-43f5-8433-c0b14a727d41/.system_generated/logs/transcript.jsonl")

found_table1 = []
found_eq6 = []

with transcript_path.open("r", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if "TABLE I" in line or "Table I" in line or "Form Factor" in line or "\\omega(FF)" in line or "omega(FF)" in line:
            data = json.loads(line)
            content = data.get("content", "")
            if "\\begin{table" in content or "TABLE I" in content or "Form Factor" in content:
                for subline in content.split("\n"):
                    if any(k in subline for k in ["TABLE I", "table I", "Form Factor", "Barcelona", "Quito", "omega", "Eq."]):
                        found_table1.append(subline[:150])

print(f"Found matches ({len(found_table1)} lines):")
for l in found_table1[:40]:
    print("  ", l)
