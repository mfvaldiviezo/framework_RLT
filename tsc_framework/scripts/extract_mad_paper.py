import json
from pathlib import Path

transcript_path = Path("C:/Users/mfval/.gemini/antigravity-ide/brain/b16f95eb-4450-43f5-8433-c0b14a727d41/.system_generated/logs/transcript_full.jsonl")
if not transcript_path.exists():
    transcript_path = Path("C:/Users/mfval/.gemini/antigravity-ide/brain/b16f95eb-4450-43f5-8433-c0b14a727d41/.system_generated/logs/transcript.jsonl")

mad_lines = []
with transcript_path.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "MAD-Gating" in line or "MAD" in line or "gating" in line:
            data = json.loads(line)
            content = data.get("content", "")
            if "MAD" in content and "\\section" in content:
                for subline in content.split("\n"):
                    if "MAD" in subline or "gating" in subline or "Gating" in subline:
                        mad_lines.append(subline.strip()[:140])

print(f"Found {len(mad_lines)} lines mentioning MAD / gating in paper:")
for l in mad_lines[:30]:
    print("  ", l)
