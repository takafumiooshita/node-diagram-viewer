# -*- coding: utf-8 -*-
# gen_mindmap.pyw (0.01): YAML設定から最小ASCIIマインドマップを生成
# (目的) YAMLで core / data_chain / logic_chain を指定し、====▶(データ流) / ----▶(制御流) を描画

import sys, datetime, yaml

cfg_path = "mindmap_config.yaml"
out_path = "ascii_mindmap_from_yaml.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

core  = cfg.get("core", "Core Idea")
data  = [str(x) for x in cfg.get("data_chain", ["Input","Stage1","Stage2"])]
logic = [str(x) for x in cfg.get("logic_chain", ["Control","Action"])]

def chain(line, arrow):
    return f"[{line[0]}]" + "".join(f"{arrow}[{n}]" for n in line[1:])

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_line  = chain(data,  "====▶")
logic_line = chain(logic, "----▶")

art = f"""# ASCII Mindmap (Flow × Layer) | generated: {now}
# rule: ====▶ (data flow), ----▶ (control flow)

                          [{core}]
                               │
              ┌────────────────┴────────────────┐
              │                                 │
        [📂 Data Layer]                   [🔧 Logic Layer]
              │                                 │
    {data_line}
    {logic_line}

"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(art)

print(f"Wrote: {out_path}")
