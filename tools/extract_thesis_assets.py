#!/usr/bin/env python3
"""Build a semantic asset catalog for the thesis full report.

This script is intentionally repeatable. It reads the source DOCX as OOXML,
catalogs every embedded media file, maps each item to a deterministic semantic
path under docs/assets/full-report/, and writes machine/human-readable
manifests.

Existing identical images are reused by SHA-256 match. On local filesystems the
semantic asset is created as a hardlink when possible, avoiding a second disk
copy while still giving the report a clean, GitHub-friendly asset layout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from PIL import Image, UnidentifiedImageError


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

DEFAULT_SOURCE = "Birinci_donem_Buck_Converter_Serbest_Projesi.docx"
DEFAULT_OUTPUT = "docs/assets/full-report"
DEFAULT_SOURCE_MAP = "docs/source-map.md"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"}


@dataclass(frozen=True)
class MediaPreset:
    category: str
    slug: str
    media_type: str
    probable_section: str
    description: str


MEDIA_PRESETS: dict[str, MediaPreset] = {
    "image1.png": MediaPreset("power-stage", "type-3-compensator-frequency-relations", "equation-image", "Bölüm 2.1 - Frekans Seçim Kuralları ve Hesaplamalar", "Type-3 compensator frekans ilişkileri"),
    "image2.png": MediaPreset("power-stage", "frequency-ordering", "technical-figure", "Bölüm 2.1 - Frekans Seçim Kuralları ve Hesaplamalar", "Frekansların büyüklük sırasına göre dizilimi"),
    "image3.png": MediaPreset("power-stage", "updated-power-stage-calculation-flow", "technical-figure", "Bölüm 3 - Güç Katı Hesaplamaları", "Güncellenmiş güç katı hesap akışı/devre görseli"),
    "image4.jpeg": MediaPreset("power-stage", "duty-cycle-36v-ltspice-check", "simulation-screenshot", "Bölüm 3 - Güç Katı Hesaplamaları", "36 V giriş için duty-cycle LTspice kontrolü"),
    "image5.png": MediaPreset("power-stage", "duty-cycle-24v-ltspice-check", "simulation-screenshot", "Bölüm 3 - Güç Katı Hesaplamaları", "24 V giriş için duty-cycle LTspice kontrolü"),
    "image6.png": MediaPreset("state-equations", "buck-converter-state-equations", "equation-image", "Bölüm 4 - Çevirici Durum Denklemleri", "Buck converter durum denklemleri"),
    "image7.png": MediaPreset("state-equations", "esr-effect-output-voltage", "technical-figure", "Bölüm 4.1 - ESR Etkisi", "ESR etkisinin çıkış gerilimi üzerindeki etkisi"),
    "image8.png": MediaPreset("state-equations", "current-voltage-general-waveforms", "waveform-diagram", "Bölüm 4.1 - ESR Etkisi", "Akım ve gerilimlerin genel dalga biçimleri"),
    "image9.png": MediaPreset("state-equations", "waveform-label-small-signal", "equation-image", "Bölüm 4.2 - Genel Dalga-Biçimleri", "Genel dalga biçimleri için küçük işaret/etiket görseli"),
    "image10.png": MediaPreset("state-equations", "waveform-equation-label", "equation-image", "Bölüm 4.2 - Genel Dalga-Biçimleri", "Genel dalga biçimleri için denklem/etiket görseli"),
    "image11.png": MediaPreset("state-equations", "buck-converter-general-waveforms", "waveform-diagram", "Bölüm 4.2 - Genel Dalga-Biçimleri", "Buck converter genel dalga biçimleri"),
    "image12.png": MediaPreset("state-equations", "decorative-small-media-12", "decorative", "Bölüm 4.2 - Genel Dalga-Biçimleri", "Kaynak DOCX küçük medya nesnesi image12"),
    "image13.png": MediaPreset("state-equations", "decorative-small-media-13", "decorative", "Bölüm 4.2 - Genel Dalga-Biçimleri", "Kaynak DOCX küçük medya nesnesi image13"),
    "image14.png": MediaPreset("controller", "controller-design-transition-diagram", "block-diagram", "Bölüm 5 - Kontrolcü Tasarımı", "Kontrolcü tasarımına geçişte kullanılan kaynak diyagram"),
    "image15.png": MediaPreset("controller", "system-block-diagram", "block-diagram", "Bölüm 5 - Kontrolcü Tasarımı", "Sistemin block diagramı"),
    "image16.png": MediaPreset("controller", "closed-loop-expression-1", "equation-image", "Bölüm 5 - Kontrolcü Tasarımı", "Kapalı çevrim ifade ilişkisi 1"),
    "image17.png": MediaPreset("controller", "closed-loop-expression-2", "equation-image", "Bölüm 5 - Kontrolcü Tasarımı", "Kapalı çevrim ifade ilişkisi 2"),
    "image18.png": MediaPreset("controller", "open-loop-transfer-function-block-expression", "equation-image", "Bölüm 5 - Kontrolcü Tasarımı", "Açık çevrim transfer fonksiyonu blok ifadesi"),
    "image19.png": MediaPreset("controller", "uncompensated-loop-gain-expression", "equation-image", "Bölüm 5 - Kontrolcü Tasarımı", "Uncompensated loop gain ifadesi"),
    "image20.png": MediaPreset("controller", "uncompensated-loop-gain-bode", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "Uncompensated loop gain Bode diyagramı"),
    "image21.png": MediaPreset("controller", "lead-compensator-bode-shape", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "Lead compensator Bode şekli"),
    "image22.png": MediaPreset("controller", "lead-compensator-frequency-response", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "Lead compensator frekans cevabı"),
    "image23.png": MediaPreset("controller", "lead-compensated-open-loop-bode", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "Lead compensator eklenmiş açık çevrim Bode diyagramı"),
    "image24.png": MediaPreset("controller", "lag-pi-compensator-bode-shape", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "Lag/PI compensator Bode şekli"),
    "image25.png": MediaPreset("controller", "pid-compensator-bode-curve", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "PID compensator Bode eğrisi"),
    "image26.png": MediaPreset("controller", "lt1215-opamp-gain-frequency", "technical-figure", "Bölüm 5 - Kontrolcü Tasarımı", "LT1215 op-amp gain-frequency grafiği"),
    "image27.png": MediaPreset("controller", "final-open-loop-bode", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "Nihai açık çevrim Bode diyagramı"),
    "image28.png": MediaPreset("controller", "calculated-open-loop-transfer-function", "equation-image", "Bölüm 5 - Kontrolcü Tasarımı", "Hesaplanan açık çevrim transfer fonksiyonu"),
    "image29.png": MediaPreset("controller", "t-of-s-closed-loop-expressions", "equation-image", "Bölüm 5 - Kontrolcü Tasarımı", "T(s)'nin kapalı çevrim ifadelerinde kullanılması"),
    "image30.png": MediaPreset("controller", "decorative-small-media-30", "decorative", "Bölüm 5 - Kontrolcü Tasarımı", "Kaynak DOCX küçük medya nesnesi image30"),
    "image31.png": MediaPreset("controller", "closed-loop-reference-to-output-response", "bode-plot", "Bölüm 5 - Kontrolcü Tasarımı", "Kapalı çevrim reference-to-output cevabı"),
    "image32.png": MediaPreset("opamp", "decorative-small-media-32", "decorative", "Bölüm 6 - Op-amp Devresi Gerçeklemesi", "Kaynak DOCX küçük medya nesnesi image32"),
    "image33.png": MediaPreset("opamp", "decorative-small-media-33", "decorative", "Bölüm 6 - Op-amp Devresi Gerçeklemesi", "Kaynak DOCX küçük medya nesnesi image33"),
    "image34.png": MediaPreset("opamp", "opamp-implementation-circuit", "circuit-diagram", "Bölüm 6 - Op-amp Devresi Gerçeklemesi", "Op-amp gerçekleştirme devresi"),
    "image35.png": MediaPreset("opamp", "sensor-gain-voltage-divider", "circuit-diagram", "Bölüm 6.1 - Sensor Gain (H(s))", "Gerilim bölücü ile H(s) sensor gain gerçekleştirmesi"),
    "image36.png": MediaPreset("opamp", "compensator-target-frequency-gain", "technical-figure", "Bölüm 6.2 - Compensator Devresi", "Compensator için hedef frekans ve kazanç davranışı"),
    "image37.png": MediaPreset("opamp", "simplified-compensator-circuit", "circuit-diagram", "Bölüm 6.2 - Compensator Devresi", "Sadeleştirilmiş compensator devresi"),
    "image38.png": MediaPreset("opamp", "r2-c2-impedance-comparison", "equation-image", "Bölüm 6.2 - Compensator Devresi", "R2 ve C2 empedans karşılaştırması"),
    "image39.png": MediaPreset("opamp", "capacitor-impedance-plus-20db-dec", "equation-image", "Bölüm 6.2 - Compensator Devresi", "Sığaç empedansının terslenmesiyle +20 dB/dec davranış"),
    "image40.png": MediaPreset("opamp", "z1-z2-impedance-network-1", "equation-image", "Bölüm 6.2 - Compensator Devresi", "Z1 ve Z2 empedans ağı 1"),
    "image41.png": MediaPreset("opamp", "z1-z2-impedance-network-2", "equation-image", "Bölüm 6.2 - Compensator Devresi", "Z1 ve Z2 empedans ağı 2"),
    "image42.png": MediaPreset("simulation", "output-power-50w-operating-point", "simulation-screenshot", "Bölüm 7.3 - Çıkış Gücü", "Yaklaşık 50 W çıkış gücü çalışma noktası"),
    "image43.png": MediaPreset("simulation", "output-power-125w-operating-point", "simulation-screenshot", "Bölüm 7.3 - Çıkış Gücü", "Yaklaşık 125 W çıkış gücü çalışma noktası"),
    "image44.png": MediaPreset("simulation", "static-output-voltage-measurement", "simulation-screenshot", "Bölüm 7.4 - Output Voltage static requirement", "Statik çıkış gerilimi ölçümü"),
    "image45.png": MediaPreset("simulation", "transient-output-voltage-load-current", "simulation-screenshot", "Bölüm 7.5 - Output Voltage transient limits", "Transient çıkış gerilimi ve yük akımı davranışı"),
    "image46.png": MediaPreset("simulation", "output-ripple-measurement", "simulation-screenshot", "Bölüm 7.6 - Allowed output voltage ripple", "Çıkış ripple ölçümü"),
    "image47.png": MediaPreset("simulation", "input-power-36v-measurement", "simulation-screenshot", "Bölüm 7.7 - Verimlilik", "36 V girişte giriş gücü ölçümü"),
    "image48.png": MediaPreset("simulation", "output-power-36v-measurement", "simulation-screenshot", "Bölüm 7.7 - Verimlilik", "36 V girişte çıkış gücü ölçümü"),
    "image49.png": MediaPreset("simulation", "output-power-24v-measurement", "simulation-screenshot", "Bölüm 7.7 - Verimlilik", "24 V girişte çıkış gücü ölçümü"),
    "image50.png": MediaPreset("simulation", "input-power-24v-measurement", "simulation-screenshot", "Bölüm 7.7 - Verimlilik", "24 V girişte giriş gücü ölçümü"),
    "image51.png": MediaPreset("future-work", "lm5146-typical-application", "circuit-diagram", "Bölüm 8 - Projenin Geleceği", "LM5146 tipik uygulama şeması"),
    "image52.png": MediaPreset("appendices", "output-capacitor-datasheet-excerpt", "datasheet-excerpt", "EK-1 - Sığaç Verisayfası", "Sığaç veri sayfası kesiti"),
    "image53.png": MediaPreset("appendices", "ltspice-circuit-overview", "circuit-diagram", "EK-2 - Genel görünüm", "LTspice devresinin genel görünümü"),
}


def repo_rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str) -> str:
    table = str.maketrans(
        {
            "ç": "c",
            "Ç": "c",
            "ğ": "g",
            "Ğ": "g",
            "ı": "i",
            "I": "i",
            "İ": "i",
            "ö": "o",
            "Ö": "o",
            "ş": "s",
            "Ş": "s",
            "ü": "u",
            "Ü": "u",
        }
    )
    clean = value.translate(table).lower()
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    return clean or "asset"


def image_number(name: str) -> int:
    match = re.search(r"image(\d+)", name, re.IGNORECASE)
    return int(match.group(1)) if match else 9999


def read_xml_from_docx(source: Path, member: str) -> ET.Element | None:
    with zipfile.ZipFile(source) as zf:
        try:
            return ET.fromstring(zf.read(member))
        except KeyError:
            return None


def paragraph_style(paragraph: ET.Element) -> str:
    style = paragraph.find("./w:pPr/w:pStyle", NS)
    if style is None:
        return ""
    return style.attrib.get(f"{{{NS['w']}}}val", "")


def paragraph_text(paragraph: ET.Element) -> str:
    chunks: list[str] = []
    for node in paragraph.iter():
        if node.tag == f"{{{NS['w']}}}t":
            chunks.append(node.text or "")
        elif node.tag == f"{{{NS['w']}}}tab":
            chunks.append("\t")
        elif node.tag == f"{{{NS['w']}}}br":
            chunks.append("\n")
        elif node.tag == f"{{{NS['m']}}}t":
            chunks.append(node.text or "")
    return " ".join("".join(chunks).split())


def is_heading_style(style: str) -> bool:
    normalized = style.lower().replace(" ", "")
    return normalized.startswith("heading") or normalized.startswith("balk") or normalized in {"title"}


def truncate(value: str, limit: int = 220) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def docx_relationships(source: Path) -> dict[str, str]:
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


def source_map_descriptions(source_map: Path) -> dict[str, dict[str, str]]:
    if not source_map.exists():
        return {}

    result: dict[str, dict[str, str]] = {}
    for line in source_map.read_text(encoding="utf-8").splitlines():
        if "docs/assets/docx-media/media/image" not in line:
            continue
        columns = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
        if len(columns) < 3:
            continue
        match = re.search(r"(image\d+\.[a-zA-Z0-9]+)", columns[0])
        if not match:
            continue
        result[match.group(1)] = {
            "probable_section": columns[1],
            "nearby_text_or_caption": columns[2],
        }
    return result


def extract_docx_media(source: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(source) as zf:
        media_members = sorted(
            (name for name in zf.namelist() if name.startswith("word/media/")),
            key=lambda value: image_number(Path(value).name),
        )
        return {Path(member).name: zf.read(member) for member in media_members}


def docx_media_events(source: Path) -> dict[str, dict[str, Any]]:
    root = read_xml_from_docx(source, "word/document.xml")
    rels = docx_relationships(source)
    if root is None:
        return {}

    body = root.find(".//w:body", NS)
    if body is None:
        return {}

    events: dict[str, dict[str, Any]] = {}
    current_heading = ""
    recent_text: list[str] = []
    order = 0

    for child in list(body):
        tag = child.tag.rsplit("}", 1)[-1]
        text = paragraph_text(child)

        if tag == "p":
            style = paragraph_style(child)
            if text and is_heading_style(style):
                current_heading = text
            elif text:
                recent_text.append(text)
                recent_text = recent_text[-4:]
        elif tag == "tbl" and text:
            recent_text.append(text)
            recent_text = recent_text[-4:]

        image_nodes: list[tuple[str, ET.Element]] = []
        image_nodes.extend(("drawingml", node) for node in child.findall(".//a:blip", NS))
        image_nodes.extend(("vml", node) for node in child.findall(".//v:imagedata", NS))

        for image_kind, node in image_nodes:
            rel_id = (
                node.attrib.get(f"{{{NS['r']}}}embed")
                or node.attrib.get(f"{{{NS['r']}}}link")
                or node.attrib.get(f"{{{NS['r']}}}id")
            )
            target = rels.get(rel_id or "", "")
            media_name = Path(target).name
            if not media_name:
                continue
            order += 1
            context = text if text and not is_heading_style(paragraph_style(child)) else " / ".join(recent_text[-2:])
            events[media_name] = {
                "relationship_id": rel_id,
                "relationship_target": target,
                "document_order": order,
                "image_kind": image_kind,
                "source_heading": current_heading,
                "nearby_text_context": truncate(context),
            }

    return events


def image_dimensions(data: bytes) -> tuple[int | None, int | None]:
    try:
        with Image.open(BytesIO(data)) as image:
            return image.size
    except UnidentifiedImageError:
        return None, None


def existing_image_hashes(repo_root: Path, output_root: Path) -> dict[str, list[Path]]:
    hashes: dict[str, list[Path]] = {}
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if output_root in path.resolve().parents or path.resolve() == output_root.resolve():
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        try:
            digest = sha256_file(path)
        except OSError:
            continue
        hashes.setdefault(digest, []).append(path)
    return hashes


def asset_preference(path: Path) -> tuple[int, str]:
    text = path.as_posix()
    if "docs/assets/docx-media/media/" in text:
        rank = 0
    elif "docs/assets/docx-media/raw/" in text:
        rank = 1
    elif "images/readme/" in text:
        rank = 2
    elif "images/docx_extracted/" in text:
        rank = 3
    else:
        rank = 4
    return rank, text.lower()


def ensure_semantic_asset(source_path: Path | None, data: bytes, target: Path) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    wanted_hash = sha256_bytes(data)

    if target.exists():
        try:
            if sha256_file(target) == wanted_hash:
                if source_path is not None and source_path.exists():
                    try:
                        if os.path.samefile(source_path, target):
                            return "hardlink-existing"
                    except OSError:
                        pass
                return "existing-target"
        except OSError:
            pass
        target.unlink()

    if source_path is not None and source_path.exists():
        try:
            os.link(source_path, target)
            return "hardlink"
        except OSError:
            shutil.copy2(source_path, target)
            return "copy-fallback"

    target.write_bytes(data)
    return "extracted-from-docx"


def build_manifest(repo_root: Path, source: Path, output_root: Path, source_map: Path) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    for folder in ["power-stage", "state-equations", "controller", "opamp", "simulation", "future-work", "appendices"]:
        (output_root / folder).mkdir(parents=True, exist_ok=True)

    extracted_media = extract_docx_media(source)
    media_events = docx_media_events(source)
    map_descriptions = source_map_descriptions(source_map)
    existing_hashes = existing_image_hashes(repo_root, output_root)

    assets: list[dict[str, Any]] = []
    for original_name, data in extracted_media.items():
        preset = MEDIA_PRESETS.get(original_name)
        if preset is None:
            stem = Path(original_name).stem
            preset = MediaPreset("uncategorized", slugify(stem), "technical-figure", "Unknown", stem)
            (output_root / preset.category).mkdir(parents=True, exist_ok=True)

        digest = sha256_bytes(data)
        matches = sorted(existing_hashes.get(digest, []), key=asset_preference)
        source_path = matches[0] if matches else None
        width, height = image_dimensions(data)
        suffix = Path(original_name).suffix.lower()
        number = image_number(original_name)
        target = output_root / preset.category / f"image{number:02d}-{preset.slug}{suffix}"
        link_method = ensure_semantic_asset(source_path, data, target)

        event = media_events.get(original_name, {})
        map_info = map_descriptions.get(original_name, {})
        source_heading = event.get("source_heading") or ""
        probable_section = map_info.get("probable_section") or preset.probable_section or source_heading or "Unknown"
        nearby_text = map_info.get("nearby_text_or_caption") or preset.description or event.get("nearby_text_context") or ""

        asset = {
            "filename": repo_rel(target, repo_root),
            "source_location": (
                f"word/media/{original_name}; "
                f"relationship={event.get('relationship_id', 'unknown')}; "
                f"image_kind={event.get('image_kind', 'unknown')}; "
                f"document_order={event.get('document_order', 'unknown')}; "
                f"source_heading={source_heading or 'unknown'}"
            ),
            "probable_section": probable_section,
            "nearby_text_or_caption": nearby_text,
            "media_type": preset.media_type,
            "reused_existing_asset": bool(matches),
            "original_media": f"word/media/{original_name}",
            "source_asset": repo_rel(source_path, repo_root) if source_path else None,
            "matching_existing_assets": [repo_rel(path, repo_root) for path in matches],
            "category": preset.category,
            "sha256": digest,
            "bytes": len(data),
            "width": width,
            "height": height,
            "link_method": link_method,
            "decorative": preset.media_type == "decorative" or len(data) < 512 or (width is not None and height is not None and width <= 3 and height <= 3),
            "nearby_text_context": event.get("nearby_text_context", ""),
        }
        assets.append(asset)

    root = read_xml_from_docx(source, "word/document.xml")
    math_count = len(root.findall(".//m:oMath", NS)) if root is not None else 0
    math_block_count = len(root.findall(".//m:oMathPara", NS)) if root is not None else 0
    equation_image_assets = [asset for asset in assets if asset["media_type"] == "equation-image"]
    decorative_assets = [asset for asset in assets if asset["decorative"]]
    reused_assets = [asset for asset in assets if asset["reused_existing_asset"]]

    return {
        "generated_by": "tools/extract_thesis_assets.py",
        "source_docx": repo_rel(source, repo_root),
        "output_root": repo_rel(output_root, repo_root),
        "asset_count": len(assets),
        "reused_existing_asset_count": len(reused_assets),
        "equation_image_asset_count": len(equation_image_assets),
        "decorative_asset_count": len(decorative_assets),
        "native_word_equation_count": math_count,
        "native_word_equation_block_count": math_block_count,
        "native_word_equation_policy": (
            "Native OMML equations are counted here but not guessed into images by this asset extractor. "
            "Embedded equation-like media are cataloged as media_type=equation-image."
        ),
        "assets": assets,
        "equation_image_assets": [
            {
                "filename": asset["filename"],
                "original_media": asset["original_media"],
                "probable_section": asset["probable_section"],
                "nearby_text_or_caption": asset["nearby_text_or_caption"],
            }
            for asset in equation_image_assets
        ],
        "decorative_assets": [
            {
                "filename": asset["filename"],
                "original_media": asset["original_media"],
                "bytes": asset["bytes"],
                "width": asset["width"],
                "height": asset["height"],
                "note": asset["nearby_text_or_caption"],
            }
            for asset in decorative_assets
        ],
    }


def write_manifest_json(manifest: dict[str, Any], output_root: Path) -> None:
    (output_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def markdown_table_row(values: list[Any]) -> str:
    cleaned = []
    for value in values:
        text = "" if value is None else str(value)
        text = text.replace("|", "\\|").replace("\n", " ")
        cleaned.append(text)
    return "| " + " | ".join(cleaned) + " |"


def write_manifest_md(manifest: dict[str, Any], output_root: Path) -> None:
    lines: list[str] = [
        "# Full Report Asset Manifest",
        "",
        "Bu manifest, kaynak DOCX içindeki görselleri ve denklem görseli gibi teknik medya varlıklarını semantik dosya adlarıyla izler.",
        "",
        "## Özet",
        "",
        f"- Kaynak DOCX: `{manifest['source_docx']}`",
        f"- Asset kökü: `{manifest['output_root']}`",
        f"- Toplam medya varlığı: {manifest['asset_count']}",
        f"- Mevcut repo görselinden yeniden kullanılan: {manifest['reused_existing_asset_count']}",
        f"- Denklem/ifade görseli olarak tutulan: {manifest['equation_image_asset_count']}",
        f"- Decorative/küçük nesne olarak işaretlenen: {manifest['decorative_asset_count']}",
        f"- Kaynak Word native denklem nesnesi: {manifest['native_word_equation_count']}",
        f"- Kaynak Word native denklem paragrafı: {manifest['native_word_equation_block_count']}",
        "",
        "Not: Native OMML denklem nesneleri bu asset çıkarıcısında tahminle kırpılmadı. DOCX içinde bitmap olarak bulunan denklem/ifade görselleri `media_type=equation-image` olarak kataloglandı.",
        "",
        "## Asset Tablosu",
        "",
        markdown_table_row(["filename", "source_location", "probable_section", "nearby_text_or_caption", "media_type", "reused_existing_asset"]),
        markdown_table_row(["---", "---", "---", "---", "---", "---"]),
    ]

    for asset in manifest["assets"]:
        lines.append(
            markdown_table_row(
                [
                    f"`{asset['filename']}`",
                    asset["source_location"],
                    asset["probable_section"],
                    asset["nearby_text_or_caption"],
                    asset["media_type"],
                    str(asset["reused_existing_asset"]).lower(),
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Yeniden Kullanılan Mevcut Görseller",
            "",
            markdown_table_row(["semantic_filename", "source_asset", "link_method", "matching_existing_assets"]),
            markdown_table_row(["---", "---", "---", "---"]),
        ]
    )
    for asset in manifest["assets"]:
        if not asset["reused_existing_asset"]:
            continue
        lines.append(
            markdown_table_row(
                [
                    f"`{asset['filename']}`",
                    f"`{asset['source_asset']}`",
                    asset["link_method"],
                    ", ".join(f"`{path}`" for path in asset["matching_existing_assets"]),
                ]
            )
        )

    lines.extend(
        [
            "",
            "## LaTeX Yerine Görsel Tutulan Denklem/İfade Varlıkları",
            "",
            markdown_table_row(["filename", "original_media", "probable_section", "nearby_text_or_caption"]),
            markdown_table_row(["---", "---", "---", "---"]),
        ]
    )
    for asset in manifest["equation_image_assets"]:
        lines.append(
            markdown_table_row(
                [
                    f"`{asset['filename']}`",
                    asset["original_media"],
                    asset["probable_section"],
                    asset["nearby_text_or_caption"],
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Decorative / Minik Nesneler",
            "",
            markdown_table_row(["filename", "original_media", "bytes", "dimensions", "note"]),
            markdown_table_row(["---", "---", "---", "---", "---"]),
        ]
    )
    for asset in manifest["decorative_assets"]:
        dimensions = f"{asset['width']}x{asset['height']}" if asset["width"] and asset["height"] else "unknown"
        lines.append(
            markdown_table_row(
                [
                    f"`{asset['filename']}`",
                    asset["original_media"],
                    asset["bytes"],
                    dimensions,
                    asset["note"],
                ]
            )
        )

    (output_root / "manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="Source DOCX path")
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT, help="Semantic asset output root")
    parser.add_argument("--source-map", default=DEFAULT_SOURCE_MAP, help="Existing source-map.md for section/caption hints")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo_root = Path.cwd()
    source = (repo_root / args.source).resolve()
    output_root = (repo_root / args.output_root).resolve()
    source_map = (repo_root / args.source_map).resolve()

    if not source.exists():
        raise SystemExit(f"Source DOCX not found: {source}")

    manifest = build_manifest(repo_root, source, output_root, source_map)
    write_manifest_json(manifest, output_root)
    write_manifest_md(manifest, output_root)

    print(f"asset_count={manifest['asset_count']}")
    print(f"reused_existing_asset_count={manifest['reused_existing_asset_count']}")
    print(f"equation_image_asset_count={manifest['equation_image_asset_count']}")
    print(f"decorative_asset_count={manifest['decorative_asset_count']}")
    print(f"manifest_json={repo_rel(output_root / 'manifest.json', repo_root)}")
    print(f"manifest_md={repo_rel(output_root / 'manifest.md', repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
