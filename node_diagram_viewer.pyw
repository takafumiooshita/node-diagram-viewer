# ファイル名：node_diagram_viewer.pyw  （v1.1）
# (目的) YAMLのノードを「座標指定」でASCII表示できるGUI。二段だけでなく列位置を明示配置。
# (使い方) 本ファイルと同じフォルダでダブルクリック実行。sample_nodes.yaml が無ければ自動生成。
# (YAML仕様・座標)
#   nodes:
#     - id: N1; label: Motor; tier: 0; col: 0   # 上段(=tier0) 左から0列目に配置
#     - id: N2; label: Driver; tier: 1; col: 3  # 下段(=tier1) 左から3列目に配置
#   links: [{from: N1, to: N2}, ...]
#   ※col省略時は自動整列。colは整数(0,1,2,…)で、1セル=4文字幅として配置
# (依存) Python 3.10 + Tkinter + PyYAML

import os, sys
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

try:
    import yaml
except Exception:
    tk.Tk().withdraw()
    messagebox.showerror("PyYAML が必要", "PyYAML が見つかりません。\n一度だけ次を実行:  py -m pip install pyyaml")
    sys.exit(1)

CELL = 4   # 列間の基本幅（1セル=4文字）

@dataclass
class Node:
    id: str
    label: str
    tier: int        # 0=上段, 1=下段
    col: Optional[int] = None  # 明示列（0起点）。未指定は自動整列

@dataclass
class Link:
    src: str
    dst: str

def load_model(path: str) -> Tuple[Dict[str, Node], List[Link]]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    nodes_raw = data.get("nodes", [])
    links_raw = data.get("links", [])

    nodes: Dict[str, Node] = {}
    for i, n in enumerate(nodes_raw, 1):
        nid = str(n.get("id", "")).strip()
        if not nid:
            raise ValueError(f"nodes[{i}] id が空")
        if nid in nodes:
            raise ValueError(f"重複ノードID: {nid}")
        tier = int(n.get("tier", 0))
        if tier not in (0, 1):
            raise ValueError(f"ノード {nid} の tier は 0/1 のみ")
        col = n.get("col", None)
        if col is not None:
            try:
                col = int(col)
                if col < 0:
                    raise ValueError
            except Exception:
                raise ValueError(f"ノード {nid} の col は 0以上の整数")
        nodes[nid] = Node(id=nid, label=str(n.get("label", nid)), tier=tier, col=col)

    links: List[Link] = []
    for j, l in enumerate(links_raw, 1):
        src = str(l.get("from", "")).strip()
        dst = str(l.get("to", "")).strip()
        if not src or not dst:
            raise ValueError(f"links[{j}] from/to が不足")
        if src not in nodes or dst not in nodes:
            raise ValueError(f"links[{j}] 未定義ノード参照: {src}->{dst}")
        links.append(Link(src=src, dst=dst))

    if not nodes:
        raise ValueError("nodes が空")
    return nodes, links

def layout(nodes: Dict[str, Node]) -> Tuple[List[Node], List[Node]]:
    top = [n for n in nodes.values() if n.tier == 0]
    bot = [n for n in nodes.values() if n.tier == 1]
    # 明示col優先→未指定はID昇順で連番colを割当
    def assign_cols(v: List[Node]):
        auto = [n for n in v if n.col is None]
        used = {n.col for n in v if n.col is not None}
        next_col = 0
        auto.sort(key=lambda x: x.id)
        for n in auto:
            while next_col in used:
                next_col += 1
            n.col = next_col
            used.add(next_col)
            next_col += 1
    assign_cols(top)
    assign_cols(bot)
    # 表示時ソートはcol→id
    top.sort(key=lambda n: (n.col, n.id))
    bot.sort(key=lambda n: (n.col, n.id))
    return top, bot

def render_ascii(nodes: Dict[str, Node], links: List[Link]) -> str:
    top, bot = layout(nodes)

    def box(n: Node) -> str:
        return f"[{n.id}:{n.label}]"

    # 先に座標（行:0/2, 列:文字index）を決める
    pos: Dict[str, Tuple[int, int]] = {}
    for n in top:
        pos[n.id] = (0, n.col * CELL)
    for n in bot:
        pos[n.id] = (2, n.col * CELL)

    # 左端がマイナスにならないよう全体をシフト（d_in対策）
    min_col = min((c for (_r, c) in pos.values()), default=0)
    shift = 1 - min(0, min_col)  # 少なくとも1は確保
    if shift:
        for k in pos:
            r, c = pos[k]
            pos[k] = (r, c + shift)

    # 必要幅を算出
    width = 1
    for nid, (r, c) in pos.items():
        need = c + len(box(nodes[nid])) + 2
        width = max(width, need)

    canvas = [list(" " * width) for _ in range(3)]

    # ノード描画（安全拡張）
    def ensure_width(w: int):
        nonlocal width, canvas
        if w > width:
            delta = w - width
            for row in range(len(canvas)):
                canvas[row].extend(" " * delta)
            width = w

    for n in top + bot:
        r, c = pos[n.id]
        s = box(n)
        ensure_width(c + len(s) + 1)
        canvas[r][c:c+len(s)] = list(s)

    # 配線（常に範囲安全）
    for lk in links:
        sr, sc = pos[lk.src]
        dr, dc = pos[lk.dst]
        s_out = sc + len(box(nodes[lk.src]))
        d_in  = max(0, dc - 1)            # 負数禁止
        mid_r = 1
        ensure_width(max(s_out, d_in) + 2)

        for r in range(min(sr, mid_r), max(sr, mid_r) + 1):
            if 0 <= s_out < width:
                canvas[r][s_out] = "+" if r == mid_r else "|"
        for r in range(min(dr, mid_r), max(dr, mid_r) + 1):
            if 0 <= d_in < width:
                canvas[r][d_in] = "+" if r == mid_r else "|"

        a, b = sorted([s_out, d_in])
        for c in range(a + 1, b):
            if 0 <= c < width:
                canvas[mid_r][c] = "-"

        if s_out < d_in and 0 <= d_in < width:
            canvas[mid_r][d_in] = ">"
        elif s_out > d_in and 0 <= s_out < width:
            canvas[mid_r][s_out] = "<"

    lines = ["".join(row).rstrip() for row in canvas]
    header = "ASCII Node Diagram (tier0=top, tier1=bottom, col=列番号×4文字)"
    return header + "\n" + "\n".join(lines) + "\n"

class App(tk.Tk):
    def __init__(self, initial_yaml: Optional[str] = None):
        super().__init__()
        self.title("Node Diagram Viewer")
        self.geometry("980x560")
        self.yaml_path: Optional[str] = initial_yaml
        self.mode = tk.StringVar(value="制作エリア")

        self.topbar = tk.Frame(self, height=6, bg="#22C55E")
        self.topbar.pack(fill="x", side="top")
        self.toolbar = tk.Frame(self); self.toolbar.pack(fill="x", pady=(2,2))
        for name, color in (("制作エリア","#2563EB"),("発想ボード","#EAB308"),("表示ビュー","#22C55E")):
            tk.Radiobutton(self.toolbar, text=name, value=name, variable=self.mode,
                           indicatoron=False, padx=10, pady=6,
                           command=lambda c=color: self.topbar.configure(bg=c)).pack(side="left", padx=2)
        tk.Button(self.toolbar, text="YAMLを開く", command=self.open_yaml).pack(side="left", padx=8)
        tk.Button(self.toolbar, text="再読み込み", command=self.reload_ascii).pack(side="left")
        tk.Button(self.toolbar, text="テキスト保存", command=self.save_text).pack(side="left", padx=8)

        self.text = ScrolledText(self, font=("Consolas", 11)); self.text.pack(fill="both", expand=True)
        self.status = tk.StringVar(value="準備完了"); tk.Label(self, textvariable=self.status, anchor="w").pack(fill="x")

        self._ensure_sample()
        self.reload_ascii()

    def open_yaml(self):
        p = filedialog.askopenfilename(title="YAMLを選択", filetypes=[("YAML","*.yaml;*.yml"),("All","*.*")])
        if p: self.yaml_path = p; self.reload_ascii()

    def reload_ascii(self):
        try:
            nodes, links = load_model(self.yaml_path)
            art = render_ascii(nodes, links)
            self._set_text(art); self.status.set(f"読み込み成功: {self.yaml_path}")
        except Exception as e:
            self._set_text(f"[ERROR]\n{e}"); self.status.set("読み込み失敗")

    def save_text(self):
        content = self.text.get("1.0", "end-1c")
        p = filedialog.asksaveasfilename(title="保存先", defaultextension=".txt", filetypes=[("Text","*.txt")])
        if p:
            try:
                with open(p, "w", encoding="utf-8") as f: f.write(content)
                self.status.set(f"保存: {p}")
            except Exception as e:
                messagebox.showerror("保存エラー", str(e))

    def _set_text(self, s: str):
        self.text.configure(state="normal"); self.text.delete("1.0","end"); self.text.insert("1.0", s); self.text.configure(state="disabled")

    def _ensure_sample(self):
        if self.yaml_path and os.path.isfile(self.yaml_path): return
        here = os.path.dirname(os.path.abspath(__file__))
        p = os.path.join(here, "sample_nodes.yaml")
        if not os.path.exists(p):
            sample = {
                "nodes": [
                    {"id":"N1","label":"Motor","tier":0,"col":0},
                    {"id":"N3","label":"Sensor","tier":0,"col":3},
                    {"id":"N2","label":"Driver","tier":1,"col":1},
                    {"id":"N4","label":"MCU","tier":1,"col":4},
                ],
                "links": [
                    {"from":"N1","to":"N2"},
                    {"from":"N3","to":"N4"},
                    {"from":"N3","to":"N2"},
                ],
            }
            with open(p, "w", encoding="utf-8") as f:
                yaml.safe_dump(sample, f, allow_unicode=True, sort_keys=False)
        self.yaml_path = p

def main():
    init_yaml = sys.argv[1] if len(sys.argv) >= 2 and os.path.isfile(sys.argv[1]) else None
    App(init_yaml).mainloop()

if __name__ == "__main__":
    main()
