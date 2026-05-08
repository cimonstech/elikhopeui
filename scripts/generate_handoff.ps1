# Regenerate handoff copies from handoff/page-map.json
Set-Location $PSScriptRoot\..
python scripts/generate_handoff.py
