# Photo Knowledge

**Keep the people and context you have confirmed with the picture.**

A photo collection can outlast the software that manages it. Names, face
rectangles, captions, and keywords should be able to travel with that collection
too. Photo Knowledge demonstrates a practical workflow: review the facts,
preview the metadata, write a portable copy, and read it back.

This small companion to [PLOS](https://github.com/bherald/personal-life-os-core)
turns that workflow into an independent reference anyone can inspect and run.
It uses established XMP, MWG region structures, and IPTC person tags. The useful
contribution is a careful review and maintenance method built around those
formats. See [the method](docs/method.md), [the format](docs/format.md), and
[maintenance](docs/maintenance.md).

Read Bill Herald's accompanying article:
[Let the photo carry its own story](docs/let-the-photo-carry-its-story.md).

## Try it

Python 3.9 or newer; no Python packages, cloud service, or PLOS installation
required. All included example identities and context are fictional. The first
manifest describes an imaginary upright 800 × 600 image. Two additional
photorealistic AI-generated portraits demonstrate metadata inside real JPEG files.

```sh
# Preview. This command writes no files.
python3 photo_knowledge.py examples/synthetic.json

# After reviewing the preview, create a new sidecar. Existing files are refused.
mkdir -p demo-output
python3 photo_knowledge.py examples/synthetic.json --output demo-output/synthetic.xmp --write

# Independently inspect it, if ExifTool is installed.
exiftool -json -struct -XMP-mwg-rs:RegionInfo -XMP-iptcExt:PersonInImage -XMP-dc:Description -XMP-dc:Subject demo-output/synthetic.xmp

python3 -m unittest discover -s tests -v
```

## See the knowledge inside a picture

| Alex Rowan — fictional label | Morgan Rowan — fictional label |
| --- | --- |
| ![AI-generated portrait with fictional label Alex Rowan](examples/photos/alex-rowan-embedded.jpg) | ![AI-generated portrait with fictional label Morgan Rowan](examples/photos/morgan-rowan-embedded.jpg) |

Photo: [Kreavo (kreavo.ai)](https://kreavo.ai/free-ai-influencer-photos),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Images resized and
fictional metadata added. The provider declares the portraits AI-generated;
these names do not identify real people. [Source and changes](examples/photos/PROVENANCE.md).

Each JPEG carries its fictional person label, manually illustrated face rectangle,
caption, keywords, and source/license credit in XMP. Move the JPEG by itself and
those fields remain in its bytes. Inspect that directly:

```sh
exiftool -json -struct -XMP:all examples/photos/alex-rowan-embedded.jpg examples/photos/morgan-rowan-embedded.jpg
```

The adjacent `.json` input, `.xmp` sidecar, `-plain.jpg` preimage, and
`-readback.json` make the before/after example inspectable. ExifTool 12.76 read
back the expected fields, and decoded pixels remained identical after embedding.
The checked examples establish this round trip; sharing services may still strip
metadata and particular catalog applications need their own qualification.

The tool checks explicit approval flags, finite coordinates, image bounds,
minimum pixel coverage, upright orientation, and a strict input field list. It
converts top-left rectangles to MWG center coordinates and emits standard XMP.
It creates sidecars only. It neither edits images nor detects or identifies
faces. A flag records the caller's approval; it cannot prove who approved it.

## What travels, and what stays private

| Portable descriptive metadata | Private working state |
| --- | --- |
| Approved face rectangles and person labels | Biometric recognition vectors |
| Reviewed caption and keywords | Unconfirmed matches and rejected suggestions |
| Optional rights and provenance fields in a complete application | Private research evidence, relationships, IDs, and audit records |

The demonstration implements the first two portable rows. It does not implement
rights/provenance management. Numerical face embeddings are model-dependent
recognition data; they are separate from descriptive XMP and are excluded here.

An XMP sidecar stays beside the picture. Embedded XMP is stored inside a supported
image file. Only the latter is literally self-contained. Sidecars need to be
copied and backed up with their images. Tools and sharing services can ignore or
strip metadata, so verify the actual destination rather than assuming survival.

For archivists, families, researchers, and collection managers, this provides a
small, testable starting point for preserving reviewed knowledge without tying
the whole collection to one database. A catalog remains useful for search,
review, history, and uncertainty. Descriptive metadata is a portable output.

## Current scope

Version 0.1.0 is a reference demonstration, not a production photo manager.
It accepts manually supplied dimensions and orientation; it does not inspect or
bind a manifest to an image hash. Do not apply the synthetic sidecar to a real
photo. Metadata merging, rotation/crop transformations, image writes, automatic
sync, identity governance, and public-export scrubbing belong to a reviewed
application workflow. [Maintenance](docs/maintenance.md) explains those gates.

ExifTool interpretation is covered by an optional integration test; tests skip
that check when the executable is absent. Compatibility with specific catalog
applications has not been certified. [Sources and attribution](NOTICE.md)
describe the standards and PLOS extraction boundary. MIT licensed; see [LICENSE](LICENSE).
