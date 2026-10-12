#!/usr/bin/env python3
"""Preview approved descriptive photo knowledge as a new XMP sidecar."""

import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {
    "x": "adobe:ns:meta/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "mwg-rs": "http://www.metadataworkinggroup.com/schemas/regions/",
    "stArea": "http://ns.adobe.com/xmp/sType/Area#",
    "stDim": "http://ns.adobe.com/xap/1.0/sType/Dimensions#",
    "Iptc4xmpExt": "http://iptc.org/std/Iptc4xmpExt/2008-02-29/",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def tag(prefix, local):
    return f"{{{NS[prefix]}}}{local}"


def keys(value, required, label):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f"{label} requires exactly: {', '.join(required)}")


def text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 4000:
        raise ValueError(f"{label} must be nonempty text of at most 4000 characters")
    # XML 1.0 excludes these controls, surrogate code points and noncharacters.
    if any(not (c in '\t\n\r' or '\u0020' <= c <= '\ud7ff'
                or '\ue000' <= c <= '\ufffd' or '\U00010000' <= c <= '\U0010ffff')
           for c in value):
        raise ValueError(f"{label} contains an invalid XML character")
    return value


def validate(data):
    keys(data, ["schema_version", "dimensions", "orientation", "description", "keywords", "regions"], "manifest")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("unsupported schema version")
    keys(data["dimensions"], ["width", "height"], "dimensions")
    for dimension in data["dimensions"].values():
        if type(dimension) is not int or dimension < 1:
            raise ValueError("dimensions must be positive integers")
    if type(data["orientation"]) is not int or data["orientation"] != 1:
        raise ValueError("only orientation 1 is supported; reconcile rotated geometry before approval")
    text(data["description"], "description")
    if not isinstance(data["keywords"], list) or len(data["keywords"]) > 100:
        raise ValueError("keywords must be a list of at most 100 entries")
    for keyword in data["keywords"]:
        text(keyword, "keyword")
    if not isinstance(data["regions"], list) or len(data["regions"]) > 100:
        raise ValueError("regions must be a list of at most 100 entries")
    for region in data["regions"]:
        keys(region, ["name", "approved", "x", "y", "w", "h"], "region")
        text(region["name"], "region name")
        if region["approved"] is not True:
            raise ValueError("every identity and region needs an explicit human approval")
        for axis in ("x", "y", "w", "h"):
            value = region[axis]
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError("region coordinates must be finite numbers")
        x, y, w, h = (region[a] for a in ("x", "y", "w", "h"))
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > 1 or y + h > 1:
            raise ValueError("region must fit within the normalized image bounds")
        if w * data["dimensions"]["width"] < 1 or h * data["dimensions"]["height"] < 1:
            raise ValueError("region must cover at least one pixel on each axis")
    return data


def build_xmp(data):
    validate(data)
    root = ET.Element(tag("x", "xmpmeta"))
    rdf = ET.SubElement(root, tag("rdf", "RDF"))
    description = ET.SubElement(rdf, tag("rdf", "Description"), {tag("rdf", "about"): ""})
    caption = ET.SubElement(description, tag("dc", "description"))
    alternative = ET.SubElement(caption, tag("rdf", "Alt"))
    ET.SubElement(alternative, tag("rdf", "li"), {"{http://www.w3.org/XML/1998/namespace}lang": "x-default"}).text = data["description"]
    for local, values, prefix in [
        ("subject", data["keywords"], "dc"),
        ("PersonInImage", list(dict.fromkeys(r["name"] for r in data["regions"])), "Iptc4xmpExt"),
    ]:
        if values:
            bag = ET.SubElement(ET.SubElement(description, tag(prefix, local)), tag("rdf", "Bag"))
            for value in values:
                ET.SubElement(bag, tag("rdf", "li")).text = value
    regions = ET.SubElement(description, tag("mwg-rs", "Regions"), {tag("rdf", "parseType"): "Resource"})
    ET.SubElement(regions, tag("mwg-rs", "AppliedToDimensions"), {
        tag("rdf", "parseType"): "Resource", tag("stDim", "w"): str(data["dimensions"]["width"]),
        tag("stDim", "h"): str(data["dimensions"]["height"]), tag("stDim", "unit"): "pixel",
    })
    bag = ET.SubElement(ET.SubElement(regions, tag("mwg-rs", "RegionList")), tag("rdf", "Bag"))
    for region in data["regions"]:
        item = ET.SubElement(bag, tag("rdf", "li"), {tag("rdf", "parseType"): "Resource"})
        ET.SubElement(item, tag("mwg-rs", "Name")).text = region["name"]
        ET.SubElement(item, tag("mwg-rs", "Type")).text = "Face"
        coordinates = {"x": region["x"] + region["w"] / 2, "y": region["y"] + region["h"] / 2,
                       "w": region["w"], "h": region["h"]}
        ET.SubElement(item, tag("mwg-rs", "Area"), {
            tag("rdf", "parseType"): "Resource", tag("stArea", "unit"): "normalized",
            **{tag("stArea", axis): format(value, ".12g") for axis, value in coordinates.items()},
        })
    ET.indent(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def create_sidecar(path, payload):
    if path.suffix.lower() != ".xmp":
        raise ValueError("output must be a new .xmp file")
    # Exclusive creation refuses existing files and existing symlinks.
    with path.open("xb") as handle:
        handle.write(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, help="new .xmp path; requires --write")
    parser.add_argument("--write", action="store_true", help="explicitly create the previewed sidecar")
    args = parser.parse_args()
    try:
        if args.write != (args.output is not None):
            raise ValueError("use --output and --write together, or neither for a read-only preview")
        if args.manifest.stat().st_size > 256 * 1024:
            raise ValueError("manifest exceeds the 256 KiB demonstration limit")
        payload = build_xmp(json.loads(args.manifest.read_text(encoding="utf-8")))
        if args.write:
            create_sidecar(args.output, payload)
            print(f"Created new sidecar: {args.output}")
        else:
            sys.stdout.buffer.write(payload)
    except (OSError, ValueError) as error:
        parser.exit(2, f"photo-knowledge: {error}\n")


if __name__ == "__main__":
    main()
