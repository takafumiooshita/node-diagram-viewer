# -*- coding: utf-8 -*-
# gen_mindmap.pyw 0.03: Flow × Layer 並列（左右）+ 矢印一覧
import yaml, datetime, textwrap

cfg = yaml.safe_load(open("mindmap_config.yaml", encoding="utf-8"))

COLW = 28   # 各カラムの幅
IND   = 2   # depth→インデント係数

def col_line(text):   # 幅に収める
    t = text[:COLW-1]
    return t + " "*(COLW-len(t))

def stamp(nodes, sym):
    # depthに応じて階段状に配置した文字列行群を返す
    lines = []
    for n in nodes:
        ind = " " * ((n.get("depth",1)-1)*IND)
        lbl = f"[{sym} {n['name']}]"
        lines.append(ind + lbl)
    return lines

def render_two_columns(core, left_nodes, right_nodes):
    L = stamp(left_nodes,  "📂")   # Data
    R = stamp(right_nodes, "🔧")   # Logic
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
        lines.append(f"  [{f['from']}] {arrow} [{f['to']}]")
    return "\n".join(lines)

core   = cfg["core"]
left   = [n for n in cfg["data_layers"]  if n.get("side","left")=="left"]
right  = [n for n in cfg["logic_layers"] if n.get("side","right")=="right"]

art = []
art.append("# ASCII Mindmap (Flow × Layer)")
art.append(f"# generated: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
art.append("")
art.append(render_two_columns(core, left, right))
art.append("")
art.append(flows_section("== Data Flows ==",  cfg.get("flows_data",  []), "====▶"))
art.append(flows_section("== Control Flows ==", cfg.get("flows_logic", []), "----▶"))
art.append("")

open("ascii_mindmap_flow_layer.txt","w",encoding="utf-8").write("\n".join(art))
print("✅ ascii_mindmap_flow_layer.txt generated.")
