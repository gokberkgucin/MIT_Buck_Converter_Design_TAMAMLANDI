#!/usr/bin/env python3
"""Convert the source DOCX report into repo-friendly Markdown.

The converter is intentionally repeatable:

- It creates the expected docs/assets directory tree.
- It prefers Pandoc when available.
- It always extracts the raw DOCX media with Python so image loss is auditable.
- It writes docs/full-report.md and docs/TRANSFER_AUDIT.md.

The Python fallback is conservative. It keeps text, headings, images, simple
tables, and math placeholders rather than silently dropping content.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import textwrap
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}

DEFAULT_SOURCE = "Birinci_donem_Buck_Converter_Serbest_Projesi.docx"
DEFAULT_PDF = "Birinci_donem_Buck_Converter_Serbest_Projesi.pdf"
MOJIBAKE_PATTERNS = ("�", "Â", "â€", "â€“", "â€”", "âœ", "Î", "ğŸ", "Ã")


@dataclass
class SourceStats:
    heading_count: int
    headings: list[tuple[int, str, str]]
    media_count: int
    tables_count: int
    list_paragraph_count: int
    math_count: int
    math_block_count: int
    math_inline_count: int
    drawings_count: int
    raw_media_files: list[Path]


@dataclass
class TargetStats:
    heading_count: int
    linked_image_count: int
    linked_images: list[str]
    table_count: int
    list_count: int
    math_count: int
    mojibake_hits: dict[str, int]
    empty_headings: list[str]


def repo_rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def clean_filename(name: str) -> str:
    stem = Path(name).stem.lower()
    suffix = Path(name).suffix.lower()
    replacements = {
        "ı": "i",
        "ğ": "g",
        "ü": "u",
        "ş": "s",
        "ö": "o",
        "ç": "c",
        "İ": "i",
        "Ğ": "g",
        "Ü": "u",
        "Ş": "s",
        "Ö": "o",
        "Ç": "c",
    }
    for src, dst in replacements.items():
        stem = stem.replace(src, dst)
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return f"{stem or 'asset'}{suffix}"


def ensure_tree(docs_dir: Path) -> dict[str, Path]:
    paths = {
        "docs": docs_dir,
        "assets": docs_dir / "assets",
        "docx_media": docs_dir / "assets" / "docx-media",
        "docx_media_raw": docs_dir / "assets" / "docx-media" / "raw",
        "figures": docs_dir / "assets" / "figures",
        "screenshots": docs_dir / "assets" / "screenshots",
        "originals": docs_dir / "originals",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    for keep_dir in (paths["figures"], paths["screenshots"]):
        (keep_dir / ".gitkeep").touch()
    return paths


def read_xml_from_docx(source: Path, member: str) -> ET.Element | None:
    with zipfile.ZipFile(source) as zf:
        try:
            return ET.fromstring(zf.read(member))
        except KeyError:
            return None


def read_relationships(source: Path) -> dict[str, str]:
    root = read_xml_from_docx(source, "word/_rels/document.xml.rels")
    if root is None:
        return {}

    rels: dict[str, str] = {}
    for rel in root:
        rel_id = rel.attrib.get("Id")
        target = rel.attrib.get("Target", "")
        if rel_id:
            rels[rel_id] = target
    return rels


def extract_raw_media(source: Path, raw_dir: Path) -> list[Path]:
    extracted: list[Path] = []
    with zipfile.ZipFile(source) as zf:
        names = sorted(name for name in zf.namelist() if name.startswith("word/media/"))
        for member in names:
            original_name = Path(member).name
            target = raw_dir / clean_filename(original_name)
            target.write_bytes(zf.read(member))
            extracted.append(target)
    return extracted


def paragraph_style(paragraph: ET.Element) -> str:
    p_style = paragraph.find("./w:pPr/w:pStyle", NS)
    if p_style is None:
        return ""
    return p_style.attrib.get(f"{{{NS['w']}}}val", "")


def paragraph_text(paragraph: ET.Element) -> str:
    chunks: list[str] = []
    for node in paragraph.iter():
        tag = node.tag
        if tag == f"{{{NS['w']}}}t":
            chunks.append(node.text or "")
        elif tag == f"{{{NS['w']}}}tab":
            chunks.append("\t")
        elif tag == f"{{{NS['w']}}}br":
            chunks.append("\n")
        elif tag == f"{{{NS['m']}}}t":
            chunks.append(node.text or "")
    return "".join(chunks).strip()


def math_text(element: ET.Element) -> str:
    parts = [node.text or "" for node in element.iter(f"{{{NS['m']}}}t")]
    return " ".join("".join(parts).split())


def source_stats(source: Path, raw_media_files: list[Path]) -> SourceStats:
    root = read_xml_from_docx(source, "word/document.xml")
    if root is None:
        raise RuntimeError("word/document.xml not found in source DOCX")

    headings: list[tuple[int, str, str]] = []
    for paragraph in root.findall(".//w:p", NS):
        style = paragraph_style(paragraph)
        text = paragraph_text(paragraph)
        if not text:
            continue
        level = heading_level(style)
        if level:
            headings.append((level, style, text))

    o_math = root.findall(".//m:oMath", NS)
    o_math_para = root.findall(".//m:oMathPara", NS)
    inline_estimate = max(0, len(o_math) - len(o_math_para))
    list_paragraphs = [
        paragraph
        for paragraph in root.findall(".//w:p", NS)
        if paragraph.find("./w:pPr/w:numPr", NS) is not None
    ]

    return SourceStats(
        heading_count=len(headings),
        headings=headings,
        media_count=len(raw_media_files),
        tables_count=len(root.findall(".//w:tbl", NS)),
        list_paragraph_count=len(list_paragraphs),
        math_count=len(o_math),
        math_block_count=len(o_math_para),
        math_inline_count=inline_estimate,
        drawings_count=len(root.findall(".//w:drawing", NS)),
        raw_media_files=raw_media_files,
    )


def heading_level(style: str) -> int:
    normalized = style.lower().replace(" ", "")
    localized = {
        "balk1": 1,
        "balk2": 2,
        "balk3": 3,
        "altyaz": 2,
    }
    if normalized in localized:
        return localized[normalized]
    if normalized == "subtitle":
        return 2
    match = re.fullmatch(r"heading([1-6])", normalized)
    if match:
        return int(match.group(1))
    return 0


def find_pandoc() -> str | None:
    return shutil.which("pandoc")


def run_pandoc(source: Path, docs_dir: Path, output_md: Path) -> tuple[str, str]:
    pandoc = find_pandoc()
    if not pandoc:
        raise RuntimeError("pandoc not found")

    cmd = [
        pandoc,
        str(source.resolve()),
        "--from=docx",
        "--to=gfm+tex_math_dollars",
        "--wrap=none",
        "--extract-media=assets/docx-media",
        "--output",
        output_md.name,
    ]
    proc = subprocess.run(
        cmd,
        cwd=docs_dir,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "pandoc failed\nSTDOUT:\n"
            + proc.stdout
            + "\nSTDERR:\n"
            + proc.stderr
        )

    rewrite_pandoc_markdown(output_md)
    return proc.stdout, proc.stderr


def rewrite_pandoc_markdown(output_md: Path) -> None:
    text = output_md.read_text(encoding="utf-8")
    # Pandoc may emit Windows separators when paths are supplied on Windows.
    text = text.replace("\\", "/")
    # Keep links relative to docs/full-report.md.
    text = text.replace("(docs/assets/", "(assets/")
    text = text.replace('"docs/assets/', '"assets/')
    output_md.write_text(text, encoding="utf-8", newline="\n")


def convert_fallback(source: Path, output_md: Path, docs_dir: Path) -> list[str]:
    root = read_xml_from_docx(source, "word/document.xml")
    if root is None:
        raise RuntimeError("word/document.xml not found in source DOCX")

    rels = read_relationships(source)
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("DOCX body not found")

    lines: list[str] = []
    unresolved: list[str] = []
    list_counter = 0

    for child in body:
        if child.tag == f"{{{NS['w']}}}p":
            style = paragraph_style(child)
            level = heading_level(style)
            text = paragraph_text(child)
            image_lines = image_markdown_for_paragraph(child, rels)
            math_lines = math_markdown_for_paragraph(child, len(unresolved) + 1)

            if math_lines and not text:
                unresolved.extend(math_lines)

            if not text and not image_lines and not math_lines:
                continue

            if level:
                lines.append(f"{'#' * level} {text or 'Untitled'}")
            elif style.lower().startswith("toc"):
                lines.append(text)
            elif is_numbered_paragraph(child):
                list_counter += 1
                lines.append(f"{list_counter}. {text}")
            elif style.lower() == "listparagraph":
                lines.append(f"- {text}")
            else:
                list_counter = 0
                if text:
                    lines.append(text)

            lines.extend(image_lines)
            if math_lines:
                for index, math in enumerate(math_lines, start=1):
                    placeholder = f"[Equation placeholder {len(unresolved) + index}: {math}]"
                    lines.append(placeholder)
            lines.append("")

        elif child.tag == f"{{{NS['w']}}}tbl":
            lines.extend(table_to_markdown(child))
            lines.append("")

    output_md.write_text("\n".join(lines).strip() + "\n", encoding="utf-8", newline="\n")
    return unresolved


def is_numbered_paragraph(paragraph: ET.Element) -> bool:
    return paragraph.find("./w:pPr/w:numPr", NS) is not None


def image_markdown_for_paragraph(paragraph: ET.Element, rels: dict[str, str]) -> list[str]:
    links: list[str] = []
    for blip in paragraph.findall(".//a:blip", NS):
        embed = blip.attrib.get(f"{{{NS['r']}}}embed")
        if not embed:
            continue
        target = rels.get(embed, "")
        if not target:
            continue
        name = clean_filename(Path(target).name)
        links.append(f"![{Path(name).stem}](assets/docx-media/raw/{name})")
    return links


def math_markdown_for_paragraph(paragraph: ET.Element, start_index: int) -> list[str]:
    values: list[str] = []
    for math_node in paragraph.findall(".//m:oMath", NS):
        text = math_text(math_node)
        if text:
            values.append(text)
        else:
            values.append(f"unresolved-ooxml-equation-{start_index + len(values):03d}")
    return values


def table_to_markdown(table: ET.Element) -> list[str]:
    rows: list[list[str]] = []
    for row in table.findall("./w:tr", NS):
        cells: list[str] = []
        for cell in row.findall("./w:tc", NS):
            text = " ".join(paragraph_text(p) for p in cell.findall(".//w:p", NS))
            text = re.sub(r"\s+", " ", text).strip()
            cells.append(text.replace("|", "\\|"))
        if cells:
            rows.append(cells)

    if not rows:
        return []

    width = max(len(row) for row in rows)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    header = normalized[0]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    for row in normalized[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def target_stats(markdown: str) -> TargetStats:
    heading_matches = re.findall(r"(?m)^#{1,6}\s+.+$", markdown)
    linked_images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", markdown)
    html_images = re.findall(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", markdown, flags=re.I)
    all_images = linked_images + html_images

    table_count = count_markdown_tables(markdown) + len(re.findall(r"<table\b", markdown, flags=re.I))
    list_count = len(re.findall(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+\S", markdown))
    math_count = count_math(markdown)
    mojibake_hits = {pattern: markdown.count(pattern) for pattern in MOJIBAKE_PATTERNS if pattern in markdown}
    empty_headings = find_empty_headings(markdown)

    return TargetStats(
        heading_count=len(heading_matches),
        linked_image_count=len(all_images),
        linked_images=all_images,
        table_count=table_count,
        list_count=list_count,
        math_count=math_count,
        mojibake_hits=mojibake_hits,
        empty_headings=empty_headings,
    )


def count_markdown_tables(markdown: str) -> int:
    lines = markdown.splitlines()
    count = 0
    in_table = False
    for index, line in enumerate(lines):
        is_separator = bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line))
        if is_separator and index > 0 and "|" in lines[index - 1]:
            if not in_table:
                count += 1
                in_table = True
        elif not line.strip() or "|" not in line:
            in_table = False
    return count


def count_math(markdown: str) -> int:
    block = len(re.findall(r"\$\$.*?\$\$", markdown, flags=re.S))
    inline = len(re.findall(r"(?<!\$)\$[^$\n]+\$(?!\$)", markdown))
    bracket = len(re.findall(r"\\\[(.*?)\\\]", markdown, flags=re.S))
    paren = len(re.findall(r"\\\((.*?)\\\)", markdown, flags=re.S))
    return block + inline + bracket + paren


def find_empty_headings(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+\S", line):
            headings.append((i, line.strip()))

    empty: list[str] = []
    for idx, (line_no, heading) in enumerate(headings):
        next_line = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        content = [line.strip() for line in lines[line_no + 1 : next_line] if line.strip()]
        if not content:
            empty.append(heading)
    return empty


def copy_originals(source: Path, repo_root: Path, originals_dir: Path) -> list[Path]:
    copied: list[Path] = []
    for path in (source, repo_root / DEFAULT_PDF):
        if path.exists():
            target = originals_dir / clean_filename(path.name)
            shutil.copy2(path, target)
            copied.append(target)
    return copied


def unresolved_equations(source: Path, target: TargetStats, limit: int = 80) -> list[str]:
    root = read_xml_from_docx(source, "word/document.xml")
    if root is None:
        return ["DOCX XML could not be read."]

    source_math = root.findall(".//m:oMath", NS)
    gap = max(0, len(source_math) - target.math_count)
    if gap == 0:
        return []

    items: list[str] = []
    for i, math_node in enumerate(source_math[: min(gap, limit)], start=1):
        text = math_text(math_node)
        if not text:
            text = "OOXML math object without extractable plain text"
        items.append(f"equation-{i:03d}: {text[:160]}")
    if gap > limit:
        items.append(f"... {gap - limit} more potential unresolved equations")
    return items


def unresolved_tables_and_lists(source: SourceStats, target: TargetStats) -> list[str]:
    issues: list[str] = []
    if target.table_count < source.tables_count:
        missing = source.tables_count - target.table_count
        issues.append(
            f"{missing} source table(s) may need manual review "
            f"(source={source.tables_count}, target_detected={target.table_count})."
        )
    if source.list_paragraph_count and target.list_count < max(1, source.list_paragraph_count // 2):
        issues.append(
            "List transfer needs manual review "
            f"(source_numbered_or_bulleted_paragraphs={source.list_paragraph_count}, "
            f"target_detected_lists={target.list_count})."
        )
    return issues


def unlinked_media(source: SourceStats, target: TargetStats) -> list[str]:
    linked_basenames = {Path(link.split("#", 1)[0].split("?", 1)[0]).name for link in target.linked_images}
    raw_basenames = {path.name for path in source.raw_media_files}
    missing = sorted(raw_basenames - linked_basenames)
    return missing


def write_transfer_audit(
    audit_path: Path,
    repo_root: Path,
    source: Path,
    output_md: Path,
    method: str,
    pandoc_stdout: str,
    pandoc_stderr: str,
    source_stats_value: SourceStats,
    target_stats_value: TargetStats,
    copied_originals: list[Path],
) -> dict[str, int]:
    unresolved_eqs = unresolved_equations(source, target_stats_value)
    table_list_issues = unresolved_tables_and_lists(source_stats_value, target_stats_value)
    missing_media = unlinked_media(source_stats_value, target_stats_value)

    manual_sections = [
        "docs/full-report.md: Control/Kontrolcu Tasarimi equations and loop-gain derivations",
        "docs/full-report.md: Op-amp compensator component equations",
        "docs/full-report.md: Benzetim sonuclari image captions and LTspice evidence mapping",
        "docs/full-report.md: Kaynaklar and ekler",
    ]
    if missing_media:
        manual_sections.append("docs/assets/docx-media: unlinked media mapping")
    if target_stats_value.mojibake_hits:
        manual_sections.append("docs/full-report.md: mojibake/encoding cleanup")
    if target_stats_value.empty_headings:
        manual_sections.append("docs/full-report.md: empty heading backfill")

    lines: list[str] = []
    lines.append("# Transfer Audit")
    lines.append("")
    lines.append("This file is generated by `tools/convert_docx_to_markdown.py`.")
    lines.append("")
    lines.append("## Conversion Summary")
    lines.append("")
    lines.append(f"- Method used: `{method}`")
    lines.append(f"- Source DOCX: `{repo_rel(source, repo_root)}`")
    lines.append(f"- Target Markdown: `{repo_rel(output_md, repo_root)}`")
    lines.append(
        "- Original copies: "
        + (
            ", ".join(f"`{repo_rel(path, repo_root)}`" for path in copied_originals)
            if copied_originals
            else "none"
        )
    )
    lines.append("")
    lines.append("## Required Metrics")
    lines.append("")
    lines.append(f"- Source heading count: `{source_stats_value.heading_count}`")
    lines.append(f"- Target heading count: `{target_stats_value.heading_count}`")
    lines.append(f"- Source extracted media count: `{source_stats_value.media_count}`")
    lines.append(f"- Target linked image count: `{target_stats_value.linked_image_count}`")
    lines.append(f"- Source table count: `{source_stats_value.tables_count}`")
    lines.append(f"- Target detected table count: `{target_stats_value.table_count}`")
    lines.append(f"- Source list paragraph count: `{source_stats_value.list_paragraph_count}`")
    lines.append(f"- Target detected list item count: `{target_stats_value.list_count}`")
    lines.append(f"- Source OOXML math object count: `{source_stats_value.math_count}`")
    lines.append(f"- Target detected math expression count: `{target_stats_value.math_count}`")
    lines.append(f"- Source drawing count: `{source_stats_value.drawings_count}`")
    lines.append("")
    lines.append("## Source Headings")
    lines.append("")
    for level, style, title in source_stats_value.headings:
        lines.append(f"- H{level} `{style}`: {title}")
    lines.append("")
    lines.append("## Unlinked Media")
    lines.append("")
    if missing_media:
        lines.append("The following extracted DOCX media files are not directly linked from `docs/full-report.md`:")
        lines.append("")
        for item in missing_media:
            lines.append(f"- `docs/assets/docx-media/raw/{item}`")
    else:
        lines.append("No unlinked media detected by basename comparison.")
    lines.append("")
    lines.append("## Unresolved Equations")
    lines.append("")
    if unresolved_eqs:
        lines.append(
            "Potential unresolved equations were detected by comparing OOXML math object count "
            "with Markdown math markers. These require manual review:"
        )
        lines.append("")
        for item in unresolved_eqs:
            lines.append(f"- {item}")
    else:
        lines.append("No unresolved equations detected by the current automated checks.")
    lines.append("")
    lines.append("## Unresolved Tables And Lists")
    lines.append("")
    if table_list_issues:
        for item in table_list_issues:
            lines.append(f"- {item}")
    else:
        lines.append("No unresolved table/list transfer issues detected by the current automated checks.")
    lines.append("")
    lines.append("## Broken Character Check")
    lines.append("")
    if target_stats_value.mojibake_hits:
        lines.append("Potential mojibake patterns detected:")
        lines.append("")
        for pattern, count in target_stats_value.mojibake_hits.items():
            lines.append(f"- `{pattern}`: {count}")
    else:
        lines.append("No common mojibake patterns detected.")
    lines.append("")
    lines.append("## Empty Subheadings")
    lines.append("")
    if target_stats_value.empty_headings:
        for heading in target_stats_value.empty_headings:
            lines.append(f"- `{heading}`")
    else:
        lines.append("No empty Markdown headings detected.")
    lines.append("")
    lines.append("## Manual Fix Sections")
    lines.append("")
    for item in manual_sections:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Pandoc Output")
    lines.append("")
    if pandoc_stdout.strip():
        lines.append("### stdout")
        lines.append("")
        lines.append("```text")
        lines.append(pandoc_stdout.strip())
        lines.append("```")
        lines.append("")
    if pandoc_stderr.strip():
        lines.append("### stderr")
        lines.append("")
        lines.append("```text")
        lines.append(pandoc_stderr.strip())
        lines.append("```")
        lines.append("")
    if not pandoc_stdout.strip() and not pandoc_stderr.strip():
        lines.append("Pandoc produced no stdout/stderr messages.")
        lines.append("")

    audit_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")

    return {
        "unresolved_equations": len(unresolved_eqs),
        "unlinked_media": len(missing_media),
        "table_list_issues": len(table_list_issues),
        "empty_headings": len(target_stats_value.empty_headings),
        "mojibake_patterns": sum(target_stats_value.mojibake_hits.values()),
    }


def maybe_append_placeholders(output_md: Path, unresolved_eqs: list[str]) -> None:
    if not unresolved_eqs:
        return
    text = output_md.read_text(encoding="utf-8")
    if "## Automated Equation Transfer Placeholders" in text:
        return

    lines = [
        "",
        "## Automated Equation Transfer Placeholders",
        "",
        "The converter detected possible OOXML math objects that need manual verification. "
        "These placeholders prevent silent equation loss during the first migration pass.",
        "",
    ]
    for item in unresolved_eqs:
        safe = item.replace("$", "\\$")
        lines.append(f"- `{safe}`")
    output_md.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="Source DOCX path")
    parser.add_argument("--docs-dir", default="docs", help="Output docs directory")
    parser.add_argument(
        "--method",
        choices=("auto", "pandoc", "python"),
        default="auto",
        help="Conversion method. auto prefers pandoc.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path.cwd()
    source = (repo_root / args.source).resolve()
    if not source.exists():
        raise SystemExit(f"Source DOCX not found: {args.source}")

    docs_dir = (repo_root / args.docs_dir).resolve()
    paths = ensure_tree(docs_dir)
    output_md = docs_dir / "full-report.md"
    audit_path = docs_dir / "TRANSFER_AUDIT.md"

    copied_originals = copy_originals(source, repo_root, paths["originals"])
    raw_media_files = extract_raw_media(source, paths["docx_media_raw"])
    source_stats_value = source_stats(source, raw_media_files)

    method_used = "python-fallback"
    pandoc_stdout = ""
    pandoc_stderr = ""
    fallback_unresolved: list[str] = []

    if args.method in ("auto", "pandoc") and find_pandoc():
        method_used = "pandoc"
        pandoc_stdout, pandoc_stderr = run_pandoc(source, docs_dir, output_md)
    elif args.method == "pandoc":
        raise SystemExit("Pandoc requested but not found.")
    else:
        fallback_unresolved = convert_fallback(source, output_md, docs_dir)

    markdown = output_md.read_text(encoding="utf-8")
    target_stats_value = target_stats(markdown)
    unresolved_eqs = unresolved_equations(source, target_stats_value)
    if fallback_unresolved:
        unresolved_eqs.extend(fallback_unresolved)
    maybe_append_placeholders(output_md, unresolved_eqs)

    # Recompute after optional placeholder insertion.
    markdown = output_md.read_text(encoding="utf-8")
    target_stats_value = target_stats(markdown)
    counts = write_transfer_audit(
        audit_path=audit_path,
        repo_root=repo_root,
        source=source,
        output_md=output_md,
        method=method_used,
        pandoc_stdout=pandoc_stdout,
        pandoc_stderr=pandoc_stderr,
        source_stats_value=source_stats_value,
        target_stats_value=target_stats_value,
        copied_originals=copied_originals,
    )

    summary = {
        "method": method_used,
        "source_media_count": source_stats_value.media_count,
        "target_linked_image_count": target_stats_value.linked_image_count,
        "target_heading_count": target_stats_value.heading_count,
        "unresolved_item_count": sum(counts.values()),
        "output": repo_rel(output_md, repo_root),
        "audit": repo_rel(audit_path, repo_root),
    }
    print("\n".join(f"{key}: {value}" for key, value in summary.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
