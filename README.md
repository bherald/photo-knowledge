# Photo Knowledge

A photo collection can outlast the software that manages it. I want the names, face rectangles, captions and keywords people have reviewed to travel with their pictures.

Photo Knowledge is a small working example: review the details, preview the metadata, write a new XMP sidecar, and read it back. It uses existing MWG region structures and IPTC person tags. You can run it without [PLOS](https://github.com/bherald/personal-life-os-core), a cloud service or extra Python packages.

## Try it

Requires Python 3.9 or newer. The first example describes an imaginary upright 800 × 600 picture. All example names and context are fictional.

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

## See it in a picture

| Alex Rowan — fictional name | Morgan Rowan — fictional name |
| --- | --- |
| ![AI-generated portrait with fictional name Alex Rowan](examples/photos/alex-rowan-embedded.jpg) | ![AI-generated portrait with fictional name Morgan Rowan](examples/photos/morgan-rowan-embedded.jpg) |

These JPEGs contain a fictional name, an illustrated face rectangle, caption, keywords and source credit in embedded XMP. Their adjacent input files, sidecars, plain JPEGs and readback files let you compare the before and after.

Photos: [Kreavo](https://kreavo.ai/free-ai-influencer-photos), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The provider declares them AI-generated. Images were resized and fictional metadata added. [Source and changes](examples/photos/PROVENANCE.md).

Inspect the embedded fields with ExifTool:

```sh
exiftool -json -struct -XMP:all examples/photos/alex-rowan-embedded.jpg examples/photos/morgan-rowan-embedded.jpg
```

ExifTool 12.76 read back the expected fields, and decoded pixels stayed identical after embedding. Those checks cover these examples; I have not certified their import into particular photo managers.

## What the tool does

The generator creates sidecars only. It checks approval flags, finite coordinates, image bounds, minimum pixel coverage and upright orientation, then converts top-left rectangles to MWG center coordinates. Dimensions and orientation are supplied manually; the tool does not inspect the image or bind it to a file hash. An approval flag records what the caller supplied, not who approved it.

It does not recognize people, edit images, merge existing metadata or handle rotation/crop changes. The embedded JPEGs are prepared examples. Do not apply the imaginary picture's sidecar to a real photo.

## Keeping the information together

Embedded XMP stays inside the picture. Both traditional JPEG and newer JPEG XL (`.jxl`) can carry it, including names and face regions. The prepared examples here use JPEG; JPEG XL has not been tested in this project. A sidecar is a separate file and must be copied and backed up with its picture. Sharing services can strip metadata, and photo managers handle it differently, so check the files at the destination.

Reviewed names, rectangles, captions and keywords are the portable information demonstrated here. Recognition vectors, unconfirmed matches, rejected suggestions and private research or genealogy IDs stay out. Rights and provenance management are outside the generator's current scope.

Read [Let the photo carry its own story](docs/let-the-photo-carry-its-story.md), [the method](docs/method.md), [the format](docs/format.md), and [maintenance notes](docs/maintenance.md) for the design and remaining work.

Version **0.1.0**. Code: [MIT](LICENSE). [Sources and notices](NOTICE.md). The optional ExifTool integration test is skipped when ExifTool is not installed.

## Help keep it going

Thanks for taking a look. If you try the example, I would appreciate your feedback.

If this example helps with your own pictures, an [optional one-time tip](https://github.com/sponsors/bherald?frequency=one-time) helps me keep testing. It does not buy support, access, priority or a deliverable.
