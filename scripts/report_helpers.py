# -*- coding: utf-8 -*-
"""生成实验报告 DOCX 的排版辅助函数。"""
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.table import Table

SONG = "宋体"
HEI = "黑体"
KAI = "楷体"
MONO = "Consolas"


def set_run_font(run, name=SONG, size=10.5, bold=False, italic=False,
                 color=None, mono=False):
    """设置 run 的中英文字体（必须同时设置 w:eastAsia 才会对中文生效）。"""
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    latin = MONO if mono else name
    run.font.name = latin
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)
    rFonts.set(qn("w:eastAsia"), name if not mono else SONG)
    return run


def clear_cell(cell):
    """删除单元格内已有的全部段落。"""
    for p in list(cell.paragraphs):
        p._element.getparent().remove(p._element)


def clean_row(row):
    """去掉模板行自带的纵向合并与 noWrap 属性，使单元格可自由换行。"""
    for tc in row._tr.findall(qn("w:tc")):
        tcPr = tc.find(qn("w:tcPr"))
        if tcPr is None:
            continue
        for tag in ("w:vMerge", "w:noWrap"):
            el = tcPr.find(qn(tag))
            if el is not None:
                tcPr.remove(el)


def para(cell, text="", size=10.5, bold=False, name=SONG, align=None,
         indent=0.0, first_line=0.0, space_before=0, space_after=3,
         line_spacing=1.28, color=None, mono=False):
    """向单元格追加一个段落。"""
    p = cell.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    if indent:
        pf.left_indent = Inches(indent)
    if first_line:
        pf.first_line_indent = Inches(first_line)
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if text:
        set_run_font(p.add_run(text), name=name, size=size, bold=bold,
                     color=color, mono=mono)
    return p


def heading(cell, text, size=12, space_before=10, space_after=5):
    """三级标题：加粗黑体。"""
    return para(cell, text, size=size, bold=True, name=HEI,
                space_before=space_before, space_after=space_after)


def code_block(cell, code, size=8.5):
    """等宽字体代码块，首行缩进对齐。"""
    lines = code.rstrip("\n").split("\n")
    for i, line in enumerate(lines):
        para(cell, line if line.strip() else " ", size=size, name=MONO, mono=True,
             space_before=0, space_after=0, line_spacing=1.08, indent=0.10)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def set_table_borders(table, sz=4, color="7F7F7F"):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        borders.append(e)
    tblPr.append(borders)


def data_table(cell, headers, rows, widths=None, size=9.0, header_fill="DCE6F1",
               total_width=6.30):
    """在单元格内插入一张带表头底纹的三线/网格表。"""
    t = cell.add_table(rows=1 + len(rows), cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_table_borders(t)
    if widths is None:
        widths = [total_width / len(headers)] * len(headers)
    scale = total_width / sum(widths)
    widths = [w * scale for w in widths]

    for j, h in enumerate(headers):
        c = t.rows[0].cells[j]
        c.text = ""
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(1.5)
        set_run_font(p.add_run(str(h)), size=size, bold=True)
        shade(c, header_fill)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.rows[i + 1].cells[j]
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == len(headers) - 1 and len(headers) > 3 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            txt = str(v)
            set_run_font(p.add_run(txt), size=size, mono=txt.isascii() and len(txt) > 12)
    for j, w in enumerate(widths):
        for r in t.rows:
            r.cells[j].width = Inches(w)
    return t


def figure(cell, img_path, width_in=6.2, caption=None, space_before=8):
    """插入图片并居中，可附图题。"""
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(str(img_path), width=Inches(width_in))
    if caption:
        cp = cell.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after = Pt(8)
        set_run_font(cp.add_run(caption), size=9.5, bold=True, name=HEI)
    return p
