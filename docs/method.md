# The review-to-portability method

Start with a working catalog and an untouched archival original. Detection and
similarity search may suggest regions or names. Treat each suggestion as a
candidate until an authorized person confirms the region and identity. Keep
rejections and uncertain evidence in the working catalog, separate from labels
intended for a portable copy.

1. Bind the reviewed region to the exact source bytes, dimensions, and orientation.
   In a production implementation, record a content hash and a revision of the
   existing metadata. A file path alone is insufficient.
2. Make the human decision explicit. A high similarity score is not an identity
   approval. Write only the exact approved name and geometry for the reviewed
   source. Decide separately whether those names may be shared.
3. Read the existing metadata before proposing changes. Include unknown region
   extensions and unrelated fields in the preservation comparison. Show added,
   removed, and changed values; conflicts need review.
4. Preview a sidecar or a copy of the image. Retain the original and a recoverable
   metadata preimage. Do not change originals simply because the tool supports it.
5. Write the approved change only while the source and metadata revision still
   match the preview. Read it back with an independent metadata reader. Compare
   the intended values and confirm unrelated metadata and image content survived.
6. Record the result, correction history, and the relationship between original,
   sidecar, and derivative. Reopen failed or uncertain results for review.

These steps are distilled from PLOS's generic metadata workflow. The standalone
tool here covers validation, preview, coordinate conversion, and exclusive
creation of a new sidecar. Hash binding, authenticated approvals, conflict
resolution, backups, image writing, and coordinated catalog updates are method
requirements for a complete integration, not capabilities of this small tool.

## Sharing is a separate decision

Maintain separate archival and public derivatives. A private approved name may
still be unsuitable for publication. Review names, face regions, captions,
keywords, locations, dates, rights, document history, identifiers, thumbnails,
and application-specific fields before sharing. Re-read the exact export bytes.
Removing metadata does not anonymize someone visible in an image. This project
does not implement or certify an anonymization or scrubber pipeline.

## Why a companion repository

The method, formats, synthetic examples, and demonstrator are useful without the
PLOS runtime. A narrow repository gives a researcher a reproducible entry point
and makes the privacy boundary easy to inspect. PLOS remains the place for its
application integration; neither private schemas nor operational repair packets
are needed to explain the transferable idea.
