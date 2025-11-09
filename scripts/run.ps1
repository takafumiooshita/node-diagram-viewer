<# usage
pwsh scripts/run.ps1
#>
Continue = 'Stop'
if (Test-Path .\.venv\Scripts\Activate.ps1) { . .\.venv\Scripts\Activate.ps1 }
Write-Host '== Generate ASCII mindmap (stub) =='
# TODO: 実体の gen_mindmap.pyw 等に差し替え
python - <<'PY'
from pathlib import Path
out = Path('ascii_mindmap_flow_layer.txt')
out.write_text('[[stub]] Flow x Layer generated', encoding='utf-8')
print('wrote', out)
PY
git add ascii_mindmap_flow_layer.txt
git commit -m "feat: generate stub ASCII mindmap" 2>
git push
