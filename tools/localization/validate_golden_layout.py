"""Static geometry/text-fit checks; this is not a Power BI rendering test.

Requires Pillow and the actual Segoe UI font files used by the report.
"""
import argparse
import json
from pathlib import Path

from PIL import ImageFont


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--font-directory", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    report = root / "Templates/TopEvoAnalytics.Report"
    manifest = load(report / "COMPONENTS.json")
    labels = load(root / "Templates/Localization/labels.json")["labels"]
    metadata = load(root / "Templates/Localization/metadata.json")["entries"]
    caption_config = load(root / "Templates/Localization/visual-captions.json")
    components = {c["role"]: c for c in manifest["components"]}
    visuals = {}
    for role, component in components.items():
        visual = load(report / "definition/pages/ReportSection/visuals" / component["id"] / "visual.json")
        assert visual["position"] == component["position"], role
        p = visual["position"]
        assert 0 <= p["x"] < p["x"] + p["width"] <= 1280, role
        assert 0 <= p["y"] < p["y"] + p["height"] <= 720, role
        visuals[role] = visual
    items = list(visuals.items())
    for i, (role_a, visual_a) in enumerate(items):
        for role_b, visual_b in items[i + 1:]:
            a, b = visual_a["position"], visual_b["position"]
            intersects = (max(a["x"], b["x"]) < min(a["x"] + a["width"], b["x"] + b["width"])
                          and max(a["y"], b["y"]) < min(a["y"] + a["height"], b["y"] + b["height"]))
            assert not intersects, f"Overlap: {role_a}, {role_b}"
    header = visuals["header.title"]
    assert header["position"]["height"] == 48
    assert header["visual"]["objects"]["value"][0]["properties"]["fontSize"]["expr"]["Literal"]["Value"] == "20D"
    boundary = header["position"]["y"] + header["position"]["height"]
    assert boundary == 64
    for role, visual in visuals.items():
        if role not in ("header.title", "navigation.pages"):
            assert visual["position"]["y"] >= boundary + 8

    def font(points, bold=False):
        # Fourfold resolution avoids integer-pixel rounding at 10 pt.
        return ImageFont.truetype(str(args.font_directory / ("seguisb.ttf" if bold else "segoeui.ttf")), round(points * 96 / 72 * 4))

    def fit(text, points, width, bold=False):
        measured = font(points, bold).getlength(text) / 4
        assert measured * 1.1 <= width, f"Insufficient width: {text!r}: {measured:.1f} in {width} px"
        return measured

    title_line_height = sum(font(20, True).getmetrics()) / 4
    assert title_line_height <= 48 - 8
    kpi_line_height = (sum(font(10).getmetrics()) + sum(font(28, True).getmetrics())) / 4
    assert kpi_line_height + 4 <= 96 - 24
    widths = [400, 190, 190, 190, 190]
    assert sum(widths) + 32 <= 1232
    for locale in ("en-US", "de-DE", "ro-RO"):
        title_width = fit(labels["HeaderReceivablesOverview"][locale], 20, 608, True)
        for key, width in (("Branch", 168), ("DateRange", 256), ("DisplayBy", 536), ("Customer", 168)):
            fit(labels[key][locale], 10, width)
        widest_caption = 0
        for i, field in enumerate(caption_config["fields"]):
            entry = next(e for e in metadata if e["kind"] == field["kind"] and e["table"] == field["table"] and e.get("name") == field["name"])
            caption = entry["captions"].get(locale) or entry["captions"]["en-US"]
            fit(caption, 10, widths[i] - 32, True)
            if i:
                widest_caption = max(widest_caption, fit(caption, 10, 296 - 32))
        for key in ("Day", "Week", "Month", "Quarter", "Year"):
            fit(labels[key][locale], 10, 536 / 5 - 4)
        # Native pageNavigator remains English in every locale; do not imply translation.
        fit("Overview", 10, 118 - 24, True)
        print(f"{locale}: PASS static title/filter/KPI/table/navigation/TimeControl text budgets; title {title_width:.1f}px; widest KPI {widest_caption:.1f}px")
    print(f"PASS: bounds, no overlaps, header boundary/clearance; title font line {title_line_height:.2f}px in 40px content area.")
    print("NOT TESTED: Desktop rendering, parameter expansion, locale runtime, navigation translation, slicer chrome and interactions.")


if __name__ == "__main__":
    main()
