# -*- coding: utf-8 -*-
# gen_mindmap.pyw : 最小のASCIIマインドマップ自動生成（0.001版）

import sys, datetime

title = "Core Idea"
out   = "ascii_mindmap_sample.txt" if len(sys.argv) < 2 else sys.argv[1]

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

art = f"""# ASCII Mindmap (Flow × Layer)  | generated: {now}
# rule: ====▶ (data flow), ----▶ (control flow)
# node: [⚙️ control] [📂 data] [🔧 function]

                          [⚙️ {title}]
                                   │
                  ┌────────────────┴────────────────┐
                  │                                 │
            [📂 Data Layer]                    [🔧 Logic Layer]
                  │                                 │
        ┌─────────┴─────────┐           ┌──────────┴───────────┐
  [📂 Input]====▶[📂 Stage1]----▶[📂 Stage2]    [⚙️ Control]----▶[🔧 Action]
       │                         │               │                 │
   ┌───┴───┐                 ┌───┴───┐       ┌──┴──┐          ┌───┴───┐
 [Drive] [CSV]            [Clean] [Join]   [n8n] [Trig]     [Fusion] [Report]

"""

with open(out, "w", encoding="utf-8") as f:
    f.write(art)

print(f"Wrote: {out}")
