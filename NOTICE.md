# Sources and attribution

Photo Knowledge is a small companion to the PLOS project. Its generic review,
coordinate, and metadata-maintenance method was distilled from PLOS's
`FaceRegionService`, `ExifWritebackService`, and face metadata writeback
documentation. The standalone Python demonstration and this repository's
explanations were authored for this companion; runtime application code,
database schemas, private records, media, and biometric vectors were not copied.

The MIT license and PLOS Contributors notice are retained from the source
project. This repository does not change ownership or licensing of external
tools or standards.

- **XMP:** Adobe's Extensible Metadata Platform provides the metadata model and
  serialization. [Adobe XMP documentation](https://developer.adobe.com/xmp/docs/)
- **MWG region structures:** established metadata region properties, documented
  by [ExifTool's MWG tag reference](https://exiftool.sourceforge.net/TagNames/MWG.html).
- **IPTC photo metadata:** person, caption, and keyword definitions from the
  [IPTC Photo Metadata Standard 2025.1](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2025.1.html).
  The specification is published by IPTC under CC BY 4.0; linked as a reference,
  not reproduced or bundled here.
- **ExifTool:** Phil Harvey's external metadata reader/writer, used optionally for
  verification. [Structured information documentation](https://exiftool.sourceforge.net/struct.html).
  No ExifTool code is distributed in this repository.

All example labels, rectangles, and captions are synthetic and do not describe
real people or historical events. No example recognition vectors or real-person
images are included. The photorealistic synthetic portraits are separate
CC BY 4.0 assets credited to [Kreavo](https://kreavo.ai/free-ai-influencer-photos);
see [image provenance](examples/photos/PROVENANCE.md) for sources and modifications.
The repository does not claim to invent photo metadata or MWG/IPTC
formats and has not certified compatibility with every photo application.
