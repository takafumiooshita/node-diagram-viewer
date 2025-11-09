# -*- coding: utf-8 -*-
# gen_mindmap.pyw 0.04: node-id化 + カタログ(Markdown)自動生成
import yaml, datetime

COLW = 28
IND  = 2

cfg  = yaml.safe_load(open("mindmap_config.yaml", encoding="utf-8"))
core = cfg["core"]

# ID→node マップ
all_nodes = {}
for n in cfg["data_layers"] + cfg["logic_layers"]:
    all_nodes[n["id"]] = n

def stamp(nodes, sym):
    lines = []
    for n in nodes:
        ind = " " * ((n.get("depth",1)-1)*IND)
        lbl = f"[{sym} {n['name']}]"
        lines.append(ind + lbl)
    return lines

def col_line(t):
    t = t[:COLW-1]
    return t + " "*(COLW-len(t))

def render_two_columns(core, left_nodes, right_nodes):
    L = stamp(left_nodes,  "📂")  # Data
    R = stamp(right_nodes, "🔧")  # Logic
    rows = max(len(L), len(R))
    L += [""]*(rows-len(L))
    R += [""]*(rows-len(R))
    out = []
    out.append(f"[{core}]")
    out.append("│")
    out.append(col_line("┌─ [📂 Data Layer]") + "│" + col_line("[🔧 Logic Layer] ─┐"))
    for i in range(rows):
        out.append(col_line(L[i]) + "│" + col_line(R[i]))
    out.append(col_line("└" + "─"* (COLW-2)) + "┴" + col_line("─"* (COLW-1)))
    return "\n".join(out)

def flows_section(title, flows, arrow):
    if not flows: return ""
    lines = [title]
    for f in flows:
        a, b = all_nodes[f["from"]], all_nodes[f["to"]]
        lines.append(f"  [{a['name']}] {arrow} [{b['name']}]")
    return "\n".join(lines)

left  = [n for n in cfg["data_layers"]  if n.get("side","left")=="left"]
right = [n for n in cfg["logic_layers"] if n.get("side","right")=="right"]

# === ASCIIマインドマップ ===
art = []
art.append("# ASCII Mindmap (Flow × Layer, v0.04)")
art.append(f"# generated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
art.append("")
art.append(render_two_columns(core, left, right))
art.append("")
art.append(flows_section("== Data Flows ==",   cfg.get("flows_data",  []), "====▶"))
art.append(flows_section("== Control Flows ==", cfg.get("flows_logic", []), "----▶"))
art.append("")
open("ascii_mindmap_flow_layer.txt","w",encoding="utf-8").write("\n".join(art))
print("✅ ascii_mindmap_flow_layer.txt generated.")

# === 機能カタログ (Markdown) ===
def md_row(layer, n):
    return f"| {layer} | {n['id']} | {n['name']} | {n.get('desc','')} |"

lines = []
lines.append(f"# 機能カタログ（Flow × Layer, v0.04）")
lines.append("")
lines.append("| Layer | ID | Name | Description |")
lines.append("|---|---|---|---|")
for n in cfg["data_layers"]:
    lines.append(md_row("Data", n))
for n in cfg["logic_layers"]:
    lines.append(md_row("Logic", n))
lines.append("")
# フロー一覧
lines.append("## Flows")
lines.append("")
lines.append("**Data**")
for f in cfg.get("flows_data",[]):
    a, b = all_nodes[f["from"]], all_nodes[f["to"]]
    lines.append(f"- {a['id']}→{b['id']}  ({a['name']} ====▶ {b['name']})")
lines.append("")
lines.append("**Control**")
for f in cfg.get("flows_logic",[]):
    a, b = all_nodes[f["from"]], all_nodes[f["to"]]
    lines.append(f"- {a['id']}→{b['id']}  ({a['name']} ----▶ {b['name']})")
lines.append("")
open("mindmap_catalog.md","w",encoding="utf-8").write("\n".join(lines))
print("✅ mindmap_catalog.md generated.")
