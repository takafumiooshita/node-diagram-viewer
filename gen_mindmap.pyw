# -*- coding: utf-8 -*-
# gen_mindmap.pyw (0.02): depth付きの階層マインドマップ生成

import yaml, datetime

cfg = yaml.safe_load(open("mindmap_config.yaml", encoding="utf-8"))

def render_layer(nodes, arrow, symbol):
    art = ""
    for n in nodes:
        indent = "    " * (n["depth"] - 1)
        art += f"{indent}[{symbol} {n['name']}]\n"
        if n != nodes[-1]:
            art += f"{indent}{arrow}\n"
    return art

core = cfg["core"]
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

data_block = render_layer(cfg["data_layers"], "====▶", "📂")
logic_block = render_layer(cfg["logic_layers"], "----▶", "🔧")

art = f"""# ASCII Mindmap (Layered)
# generated: {now}

[{core}]
│
├── [📂 Data Layer]
{data_block}
└── [🔧 Logic Layer]
{logic_block}
"""

open("ascii_mindmap_layered.txt", "w", encoding="utf-8").write(art)
print("✅ ascii_mindmap_layered.txt generated.")
