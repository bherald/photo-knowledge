# Maintenance, corrections, and migration

Choose one owner for each metadata update. Keep a working catalog for decisions,
uncertainty, and history; maintain a reviewed portable output alongside it.
Avoid a silent two-way sync where a stale sidecar replaces a newer human decision.

## Naming corrections

Preserve the earlier label and why it changed in private review history. Confirm
the corrected identity against the exact source and region. Preview changes to
region names, PersonInImage, and any name-bearing keywords together. Review
unrelated labels and region extensions before replacement. A rename does not
automatically prove that other photographs show the same person.

## Region changes and image edits

Recheck overlays when an image is rotated, cropped, mirrored, rescanned, restored,
or replaced. Track original-to-derivative provenance. Do not reuse coordinates
based only on matching filenames. Keep actual dimensions, orientation, and
content hashes in the working manifest. Regenerating recognition vectors after
an image change belongs to the private recognition system; it must not overwrite
operator identities or publish vectors.

## Sidecars and embedded copies

Back up image/sidecar pairs together and preserve the pairing during rename or
move. A plain `.xmp` file is not cryptographically tied to its neighbor. The demo
does not detect a mismatch, merge an existing sidecar, or update one in place.
Generate a separate candidate, compare with the earlier version, and retain the
preimage under your collection's retention policy.

For supported image containers, a separate reviewed process can copy selected
XMP properties into a *disposable image copy*. With ExifTool, the selective copy
shape is:

```sh
# Only after verifying the sidecar matches this disposable image's actual source,
# dimensions, orientation, names, geometry, existing metadata, and sharing scope.
exiftool -tagsFromFile reviewed.xmp -XMP-mwg-rs:RegionInfo -XMP-iptcExt:PersonInImage -XMP-dc:Description -XMP-dc:Subject disposable-copy.jpg
exiftool -json -struct -XMP-mwg-rs:RegionInfo -XMP-iptcExt:PersonInImage -XMP-dc:Description -XMP-dc:Subject disposable-copy.jpg
```

This is a manual integration example, not a command run by the demonstrator.
ExifTool normally retains the preimage with an `_original` suffix; confirm that
behavior for your installed version and archive it before further writes. The
selected properties replace the corresponding destination values, so merging and
conflict decisions must precede execution. Never use the synthetic sidecar for a
real picture. RAW and unsupported or risky containers favor sidecars.

## Migration qualification

Test on approved copies first. Read back the structured regions, distinct person
list, caption, and keywords with ExifTool and the intended destination program.
Check the rendered overlay on upright, rotated, cropped, and multi-person cases.
Compare unrelated metadata, rights, dates, color profile, and image pixels. A
successful write command alone does not establish interoperability or preservation.

Keep a manifest of exported files and source revisions outside the published
collection if it contains private IDs or audit details. Stop on mismatched hashes,
unknown geometry conventions, lost extensions, unexpected warnings, rejected
identities, or incomplete backups. Resolve the cause before retrying.

## Public derivatives

Make a separately approved export with an explicit field policy. Inspect all
metadata families and the rendered pixels. Naming a person in a private catalog
does not grant permission to publish that name. Preserve archival originals and
rights/provenance records; removing fields from a public derivative should not
erase your private research history. Metadata cleanup is not face anonymization.

## Release maintenance

Keep the public companion's format contract and synthetic tests versioned.
When PLOS's metadata method changes, review only the relevant generic method,
adjust this independent example if needed, and rerun its checks. Do not mirror
private photo data or full operational documentation into this repository.
