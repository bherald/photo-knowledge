import copy
import json
import math
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from photo_knowledge import NS, build_xmp, create_sidecar

ROOT = Path(__file__).resolve().parents[1]


class PhotoKnowledgeTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/synthetic.json").read_text())

    def test_top_left_is_converted_to_center_and_units_are_explicit(self):
        tree = ET.fromstring(build_xmp(self.data))
        area = tree.find(".//mwg-rs:Area", NS)
        self.assertEqual(float(area.get(f"{{{NS['stArea']}}}x")), 0.35)
        self.assertEqual(float(area.get(f"{{{NS['stArea']}}}y")), 0.35)
        self.assertEqual(area.get(f"{{{NS['stArea']}}}unit"), "normalized")
        dimension = tree.find(".//mwg-rs:AppliedToDimensions", NS)
        self.assertEqual(dimension.get(f"{{{NS['stDim']}}}w"), "800")

    def test_xml_escaping_and_unicode_round_trip(self):
        self.data["regions"][0]["name"] = 'Fictional <Jo> & "Renée"'
        tree = ET.fromstring(build_xmp(self.data))
        self.assertEqual(tree.find(".//mwg-rs:Name", NS).text, self.data["regions"][0]["name"])

    def test_unapproved_region_refused(self):
        for value in [False, None, "true", 1]:
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["regions"][0]["approved"] = value
                with self.assertRaises(ValueError):
                    build_xmp(data)

    def test_unknown_fields_and_vectors_refused(self):
        for location in ["manifest", "region"]:
            data = copy.deepcopy(self.data)
            target = data if location == "manifest" else data["regions"][0]
            target["embedding"] = [0.1, 0.2]
            with self.assertRaises(ValueError):
                build_xmp(data)

    def test_nonfinite_bool_and_out_of_bounds_coordinates_refused(self):
        for axis, value in [("x", math.nan), ("y", math.inf), ("w", True), ("x", -0.01), ("h", 0), ("w", 0.9)]:
            with self.subTest(axis=axis, value=value):
                data = copy.deepcopy(self.data)
                data["regions"][0][axis] = value
                with self.assertRaises(ValueError):
                    build_xmp(data)

    def test_subpixel_regions_refused(self):
        self.data["regions"][0]["w"] = 0.00001
        with self.assertRaises(ValueError):
            build_xmp(self.data)

    def test_rotated_or_mirrored_orientation_refused(self):
        for orientation in range(2, 9):
            self.data["orientation"] = orientation
            with self.assertRaises(ValueError):
                build_xmp(self.data)

    def test_invalid_dimensions_and_xml_controls_refused(self):
        self.data["dimensions"]["width"] = True
        with self.assertRaises(ValueError):
            build_xmp(self.data)
        self.setUp()
        self.data["description"] = "bad\x00caption"
        with self.assertRaises(ValueError):
            build_xmp(self.data)

    def test_repeated_person_label_deduplicated_but_regions_retained(self):
        self.data["regions"].append(copy.deepcopy(self.data["regions"][0]))
        tree = ET.fromstring(build_xmp(self.data))
        self.assertEqual(len(tree.findall(".//Iptc4xmpExt:PersonInImage/rdf:Bag/rdf:li", NS)), 1)
        self.assertEqual(len(tree.findall(".//mwg-rs:RegionList/rdf:Bag/rdf:li", NS)), 2)

    def test_existing_file_and_symlink_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.xmp"
            output.write_bytes(b"original")
            with self.assertRaises(FileExistsError):
                create_sidecar(output, build_xmp(self.data))
            self.assertEqual(output.read_bytes(), b"original")
            link = Path(directory) / "link.xmp"
            link.symlink_to(output)
            with self.assertRaises(FileExistsError):
                create_sidecar(link, build_xmp(self.data))

    def test_cli_preview_does_not_write_and_output_requires_explicit_write(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "new.xmp"
            command = [sys.executable, str(ROOT / "photo_knowledge.py"), str(ROOT / "examples/synthetic.json")]
            preview = subprocess.run(command, capture_output=True, check=True)
            ET.fromstring(preview.stdout)
            refused = subprocess.run(command + ["--output", str(output)], capture_output=True)
            self.assertEqual(refused.returncode, 2)
            self.assertFalse(output.exists())
            subprocess.run(command + ["--output", str(output), "--write"], capture_output=True, check=True)
            self.assertEqual(output.read_bytes(), preview.stdout)

    @unittest.skipUnless(shutil.which("exiftool"), "ExifTool not installed")
    def test_exiftool_interprets_generated_sidecar(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.xmp"
            output.write_bytes(build_xmp(self.data))
            result = subprocess.run(["exiftool", "-json", "-struct", "-XMP-mwg-rs:RegionInfo", "-XMP-iptcExt:PersonInImage", str(output)], capture_output=True, text=True, check=True)
            values = json.loads(result.stdout)[0]
            self.assertNotIn("Warning", values)
            region = values["RegionInfo"]["RegionList"][0]
            self.assertEqual(region["Name"], "Synthetic Subject A")
            self.assertEqual(region["Area"]["X"], 0.35)
            self.assertEqual(values["PersonInImage"], ["Synthetic Subject A"])

    @unittest.skipUnless(shutil.which("exiftool"), "ExifTool not installed")
    def test_licensed_portraits_embedded_readback_matches_manifest(self):
        for slug in ["alex-rowan", "morgan-rowan"]:
            with self.subTest(slug=slug):
                manifest = json.loads((ROOT / "examples/photos" / f"{slug}.json").read_text())
                image = ROOT / "examples/photos" / f"{slug}-embedded.jpg"
                result = subprocess.run(["exiftool", "-json", "-struct", "-XMP:all", str(image)], capture_output=True, text=True, check=True)
                values = json.loads(result.stdout)[0]
                self.assertNotIn("Warning", values)
                region = values["RegionInfo"]["RegionList"][0]
                expected = manifest["regions"][0]
                self.assertEqual(region["Name"], expected["name"])
                self.assertAlmostEqual(region["Area"]["X"], expected["x"] + expected["w"] / 2)
                self.assertAlmostEqual(region["Area"]["Y"], expected["y"] + expected["h"] / 2)
                self.assertEqual(values["PersonInImage"], [expected["name"]])
                self.assertEqual(values["Description"], manifest["description"])
                self.assertEqual(values["Subject"], manifest["keywords"])
                self.assertIn("CC BY 4.0", values["Rights"])
                self.assertEqual(values["Creator"], ["Kreavo"])

    def test_fixture_bytes_match_public_provenance_hashes(self):
        import hashlib
        provenance = json.loads((ROOT / "examples/photos/PROVENANCE.json").read_text())
        for item in provenance:
            for name, digest in item["files"].items():
                self.assertEqual(hashlib.sha256((ROOT / "examples/photos" / name).read_bytes()).hexdigest(), digest)

    @unittest.skipUnless(shutil.which("exiftool"), "ExifTool not installed")
    def test_embedding_into_disposable_copy_preserves_preimage_and_reads_after_move(self):
        source = ROOT / "examples/photos/alex-rowan-plain.jpg"
        original = source.read_bytes()
        manifest = json.loads((ROOT / "examples/photos/alex-rowan.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            sidecar = Path(directory) / "reviewed.xmp"
            sidecar.write_bytes(build_xmp(manifest))
            target = Path(directory) / "copy.jpg"
            target.write_bytes(original)
            subprocess.run(["exiftool", "-tagsFromFile", str(sidecar), "-XMP-mwg-rs:RegionInfo", "-XMP-iptcExt:PersonInImage", "-XMP-dc:Description", "-XMP-dc:Subject", str(target)], check=True, capture_output=True)
            self.assertEqual(Path(str(target) + "_original").read_bytes(), original)
            sidecar.unlink()
            moved = Path(directory) / "independent.jpg"
            target.rename(moved)
            result = subprocess.run(["exiftool", "-json", "-struct", "-XMP:all", str(moved)], check=True, capture_output=True, text=True)
            values = json.loads(result.stdout)[0]
            self.assertEqual(values["RegionInfo"]["RegionList"][0]["Name"], "Alex Rowan")
            self.assertEqual(values["Description"], manifest["description"])
        self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
