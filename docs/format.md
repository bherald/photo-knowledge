# Metadata format

The input JSON is a demonstration contract, not a new interoperability standard.
`schema_version` is 1. Dimensions describe the actual coordinate basis. The tool
accepts orientation 1 only and requires the fields shown in
[the synthetic manifest](../examples/synthetic.json). It rejects extra fields,
including vectors or private database identifiers.

| Input | Output | Meaning |
| --- | --- | --- |
| `description` | `dc:description`, RDF language alternative | Reviewed caption, `x-default` language |
| `keywords` | `dc:subject`, RDF bag | Search labels |
| `regions[].name` | `mwg-rs:Name` and `Iptc4xmpExt:PersonInImage` | Approved label and distinct names present |
| `regions[].x/y/w/h` | `mwg-rs:Area`, `stArea` | Normalized rectangle geometry |
| `dimensions` | `mwg-rs:AppliedToDimensions`, `stDim` | Pixel dimensions used for region geometry |
| `regions[].approved` | No emitted field | Input gate; review evidence remains outside XMP |

Input `(x, y)` is the top-left corner. MWG area `(x, y)` is the center:

```text
center_x = top_left_x + width / 2
center_y = top_left_y + height / 2
```

The synthetic rectangle `(0.25, 0.20, 0.20, 0.30)` becomes center
`(0.35, 0.35)` with width `0.20` and height `0.30`. Coordinates have normalized
units; applied dimensions have pixel units. The XML property is
`mwg-rs:Regions`; ExifTool exposes its structured value as
`XMP-mwg-rs:RegionInfo`.

Orientation matters. A viewer may display rotated pixels while the stored image
has another coordinate basis. The demonstration refuses any orientation except
1 rather than guessing a transform. Before using a real workflow, inspect actual
orientation, encoded dimensions, and region overlay together. Scaling may retain
normalized geometry if the image content is unchanged; cropping, physical
rotation, mirroring, and replacement need transformed geometry and fresh review.

The IPTC Extension also defines an Image Region structure. This demonstration
uses MWG regions; it does not implement the distinct IPTC region schema or claim
that they are interchangeable. MWG and IPTC person tags likewise are descriptive
annotations, not biometric face-recognition vectors.

Primary references:

- [ExifTool MWG tags](https://exiftool.sourceforge.net/TagNames/MWG.html)
- [ExifTool structured information](https://exiftool.sourceforge.net/struct.html)
- [IPTC Photo Metadata Standard 2025.1](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2025.1.html)

No new XMP namespace is introduced. Namespaces and property identifiers are used
for interoperability; the standard documents themselves are not bundled.
