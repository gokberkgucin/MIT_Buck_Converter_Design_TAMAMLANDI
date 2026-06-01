from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CHECK_FILES = [
    Path("README.md"),
    Path("FINAL_QA.md"),
    Path("docs/index.md"),
    Path("docs/full-report.md"),
    Path("docs/verification-summary.md"),
    Path("docs/source-map.md"),
    Path("docs/TRANSFER_AUDIT.md"),
]

MOJIBAKE_PATTERNS = ["Â", "Ã", "Å", "Ä", "â€", "Î", "ğŸ", "\ufffd"]
ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"\b[A-Za-z]:[\\/][^\s)]+"),
    re.compile(r"file://", re.IGNORECASE),
]
KEY_ANCHORS = [
    "kapak",
    "abstract",
    "icindekiler",
    "giris",
    "guc-ve-kontrol-tasariminda-izlenen-yontem",
    "guc-kati-hesaplamalari",
    "cevirici-durum-denklemleri",
    "kontrolcu-tasarimi",
    "op-amp-devresi-gerceklemesi",
    "benzetim-sonuclari",
    "projenin-gelecegi",
    "kaynaklar",
    "ekler",
]
KEY_VALUES = ["49.5957", "124.1839", "1.30", "8.58", "37.38", "97.78"]


def read(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def slugify_heading(text: str) -> str:
    text = text.strip().lower()
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\s\u0080-\uffff-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def anchors_for(path: Path) -> set[str]:
    text = read(path)
    anchors = set(re.findall(r'<a\s+id="([^"]+)"\s*></a>', text))
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            anchors.add(slugify_heading(match.group(2)))
    return anchors


def local_targets(markdown: str) -> list[tuple[str, bool]]:
    targets: list[tuple[str, bool]] = []
    for match in re.finditer(r"(!)?\[[^\]]+\]\(([^)]+)\)", markdown):
        raw = match.group(2).strip()
        if not raw or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
            continue
        targets.append((raw, bool(match.group(1))))
    return targets


def split_target(raw: str) -> tuple[str, str]:
    raw = raw.split("?", 1)[0]
    if "#" in raw:
        path, anchor = raw.split("#", 1)
        return unquote(path), unquote(anchor)
    return unquote(raw), ""


def resolve_path(source: Path, target_path: str) -> Path:
    if target_path == "":
        return (ROOT / source).resolve()
    return (ROOT / source.parent / target_path).resolve()


def check_links() -> tuple[list[str], list[str]]:
    broken: list[str] = []
    missing_images: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}

    for source in CHECK_FILES:
        source_abs = ROOT / source
        if not source_abs.exists():
            broken.append(f"{source}: file itself is missing")
            continue

        for raw, is_image in local_targets(read(source)):
            target_path, anchor = split_target(raw)
            resolved = resolve_path(source, target_path)
            display = f"{source} -> {raw}"

            if target_path and not resolved.exists():
                if is_image:
                    missing_images.append(display)
                else:
                    broken.append(display)
                continue

            if anchor:
                target_rel = resolved.relative_to(ROOT) if resolved.exists() else source
                if target_rel not in anchor_cache:
                    anchor_cache[target_rel] = anchors_for(target_rel)
                if anchor not in anchor_cache[target_rel]:
                    broken.append(f"{display} (missing anchor #{anchor})")

    return broken, missing_images


def count_full_report_images() -> tuple[int, list[str]]:
    text = read(Path("docs/full-report.md"))
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    images.extend(re.findall(r'<img\s+[^>]*src="([^"]+)"', text))
    missing = []
    for raw in images:
        target_path, _ = split_target(raw)
        resolved = resolve_path(Path("docs/full-report.md"), target_path)
        if not resolved.exists():
            missing.append(raw)
    return len(images), missing


def docx_media_usage() -> tuple[int, int, list[str]]:
    text = read(Path("docs/full-report.md"))
    refs = re.findall(r"\[[^\]]+\]\((assets/(?:docx-media/media|full-report)/[^)]+)\)", text)
    refs.extend(re.findall(r'<img\s+[^>]*src="(assets/(?:docx-media/media|full-report)/[^"]+)"', text))

    semantic_to_original: dict[str, str] = {}
    manifest = ROOT / "docs/assets/full-report/manifest.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for asset in data.get("assets", []):
            filename = asset.get("filename")
            original = asset.get("original_media")
            if not filename or not original:
                continue
            semantic_to_original[Path(filename).as_posix().removeprefix("docs/")] = Path(original).name

    linked: set[str] = set()
    for ref in refs:
        if ref.startswith("assets/docx-media/media/"):
            linked.add(Path(ref).name)
        elif ref in semantic_to_original:
            linked.add(semantic_to_original[ref])

    media_dir = ROOT / "docs/assets/docx-media/media"
    media_files = sorted(path.name for path in media_dir.iterdir() if path.is_file())
    unlinked = [name for name in media_files if name not in linked]
    return len(media_files), len(linked), unlinked


def main() -> int:
    broken, missing_images = check_links()
    image_count, full_missing_images = count_full_report_images()
    docx_media_total, docx_media_linked, docx_media_unlinked = docx_media_usage()

    full = read(Path("docs/full-report.md"))
    verification = read(Path("docs/verification-summary.md"))
    source_map = read(Path("docs/source-map.md"))

    mojibake = {}
    absolute = {}
    for path in CHECK_FILES:
        if not (ROOT / path).exists():
            continue
        text = read(path)
        hits = {p: text.count(p) for p in MOJIBAKE_PATTERNS if text.count(p)}
        if hits:
            mojibake[str(path)] = hits
        abs_hits = []
        for pattern in ABSOLUTE_PATH_PATTERNS:
            abs_hits.extend(pattern.findall(text))
        if abs_hits:
            absolute[str(path)] = abs_hits

    present_anchors = anchors_for(Path("docs/full-report.md"))
    missing_key_anchors = [a for a in KEY_ANCHORS if a not in present_anchors]
    value_mismatches = [v for v in KEY_VALUES if v not in full or v not in verification]

    summary_only_hits = []
    for needle in ["summary-only", "özetledim", "özet olarak kaldı"]:
        if needle in full.lower():
            summary_only_hits.append(needle)

    todo_hits = []
    for i, line in enumerate(full.splitlines(), 1):
        if "TODO:" in line:
            todo_hits.append(f"docs/full-report.md:{i}: {line.strip()}")

    source_map_manual = "Input voltage transient" in source_map and "image12.png" in source_map

    print("QA_RESULT")
    print(f"checked_files={len(CHECK_FILES)}")
    print(f"broken_links={len(broken)}")
    for item in broken:
        print(f"  BROKEN {item}")
    print(f"missing_images={len(missing_images) + len(full_missing_images)}")
    for item in missing_images:
        print(f"  MISSING_IMAGE {item}")
    for item in full_missing_images:
        print(f"  MISSING_FULL_REPORT_IMAGE {item}")
    print(f"full_report_image_links={image_count}")
    print(f"docx_media_total={docx_media_total}")
    print(f"docx_media_unique_linked={docx_media_linked}")
    print(f"docx_media_unlinked={len(docx_media_unlinked)}")
    for item in docx_media_unlinked:
        print(f"  DOCX_MEDIA_UNLINKED {item}")
    print(f"mojibake_files={len(mojibake)}")
    for item, hits in mojibake.items():
        print(f"  MOJIBAKE {item}: {hits}")
    print(f"absolute_path_files={len(absolute)}")
    for item, hits in absolute.items():
        print(f"  ABSOLUTE {item}: {hits[:5]}")
    print(f"missing_key_anchors={len(missing_key_anchors)}")
    for item in missing_key_anchors:
        print(f"  MISSING_ANCHOR {item}")
    print(f"verification_value_mismatches={len(value_mismatches)}")
    for item in value_mismatches:
        print(f"  VALUE_MISMATCH {item}")
    print(f"summary_only_hits={len(summary_only_hits)}")
    print(f"todo_hits={len(todo_hits)}")
    for item in todo_hits:
        print(f"  TODO {item}")
    print(f"source_map_manual_items_present={source_map_manual}")
    return 0 if not broken and not missing_images and not full_missing_images else 1


if __name__ == "__main__":
    raise SystemExit(main())
