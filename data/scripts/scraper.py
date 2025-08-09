#!/usr/bin/env python3
import json, pathlib, datetime

root = pathlib.Path(__file__).resolve().parents[1]
data_path = root / "data" / "jobs.json"

payload = json.loads(data_path.read_text(encoding="utf-8"))
roles = payload.get("roles", [])

# Dedupe by (Title, Company, Location, Link)
seen = set()
deduped = []
for r in roles:
    key = (r.get("Title"), r.get("Company"), r.get("Location"), r.get("Link"))
    if key in seen:
        continue
    seen.add(key)
    deduped.append(r)

payload["roles"] = deduped
payload["generated_at"] = datetime.datetime.utcnow().isoformat() + "Z"

data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated jobs.json — roles:", len(deduped))
