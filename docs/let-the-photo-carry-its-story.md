# Let the photo carry its own story

By Bill Herald

A photograph can survive while the information that makes it useful disappears. The image gets copied to another drive, but the names remain in a photo organizer. A caption stays in somebody's notes. The next person receives the picture and has to work out who is in it and why it matters.

I want the useful information to travel with the picture. In PLOS, the personal information system I am building, that means preserving approved names and face regions in photo metadata, along with selected descriptive information. I am also preparing a small public project to explain the method without requiring someone to adopt the whole system.

Consider a made-up example. A historical society has a photograph of three volunteers restoring a community building. Its files identify Alex Morgan and Casey Reed, but the third person's name is unknown. The caption explains the work, and the photographer's credit is recorded. A useful archival copy should carry those known names, the caption and the credit. It should also leave the unknown person unknown.

A name attached to the whole image tells us someone appears in the photograph. A face region goes a step further: it connects an approved name to a particular area of the picture. That distinction becomes useful when several people appear together. It also gives the next reviewer something concrete to inspect instead of a list of names without positions.

The formats for doing this already exist. IPTC defines descriptive photo fields, including people shown in an image. XMP provides a way to store structured metadata. The Metadata Working Group region format describes areas within an image, including faces. ExifTool can read and write these structures. My work applies these established formats to a practical preservation problem. [IPTC Photo Metadata Standard](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2025.1.html), [ExifTool MWG tags](https://exiftool.org/TagNames/MWG.html).

This information can stay inside the photograph itself. Traditional JPEG files and newer JPEG XL (`.jxl`) files can both carry XMP, including names and the regions that show which face belongs to each name. That gives us a way to keep the information with the picture as file formats change. It still depends on the software reading and preserving those fields. My prepared examples use JPEG; I have not yet tested the same process with JPEG XL. [JPEG XL file format](https://jpeg.org/jpegxl/), [ExifTool JPEG XL metadata support](https://exiftool.org/TagNames/Jpeg2000.html).

There is an important difference between embedding information in a file and a face-recognition embedding. The first means saving descriptive information with the picture. The second is a numerical representation a recognition system uses to compare faces. In PLOS, those recognition vectors are stored separately in a database. They are not what I mean by letting the photo carry its story, and they do not belong in this public demonstration.

The working database still has a job. It holds review state, matching candidates and records of decisions. A picture does not need to contain every internal record to be useful outside the application. It needs a carefully chosen description that somebody has checked and is willing to share. A source reference can help point to supporting material, but a name written into metadata is still a recorded claim, not proof of identity.

For the historical society example, a sensible process starts with a copy and a review. Read what is already there. Check each proposed name and region. Show the difference before writing it. Preserve the existing photographer credit, dates and other unrelated fields. Write the approved change, then read the result back and compare it with the intended values. Keep the original and the decision record so a correction does not depend on memory.

That sequence matters when maintaining faces over time. A person may be mislabeled, a rectangle may point at the wrong face, or a later crop may change the coordinates. Correcting the catalog alone can leave an old name inside the file. Maintenance needs to include both the working record and the approved metadata output, with a fresh check of the actual image before applying the change. A previous approval should not silently authorize a different picture.

Some collections should start with an XMP sidecar, a separate metadata file stored beside the picture. It allows a demonstration without editing an original. The tradeoff is that the image and sidecar must stay together when copied or backed up. Embedding selected fields in a supported image can reduce that separation, but it requires a reliable write path and a preserved original. Different file formats and applications need their own checks.

I would test portability by reading the result in another tool and checking the actual fields. A familiar thumbnail or a successful save message is not enough. An editor may interpret a region differently, and an export or sharing service may remove metadata. Keep the archival copy separate from a social sharing copy, and verify what survives the particular route you use.

Privacy belongs in that same review. Being able to record a name does not mean every recipient should receive it. Names, locations and captions can disclose more than the visible picture. Select the fields appropriate for the recipient, especially when living people or children are involved. A demonstration can use fictional labels and a synthetic image; it does not need anyone's private collection.

The public example uses two downloaded portraits that Kreavo describes as AI-generated and licenses under Creative Commons Attribution 4.0. Alex Rowan and Morgan Rowan are fictional demonstration names. The face regions are manually illustrated metadata, not recognition results. These portraits are separate from the imagined historical-society example. Photo: [Kreavo (kreavo.ai)](https://kreavo.ai/free-ai-influencer-photos), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); demonstration copies are resized and add fictional labels and metadata.

In the prepared JPEG examples, ExifTool read-back confirms the fictional labels and region structures. This checks the saved fields; wider interoperability still needs testing.

This could help family archives, local history collections and organizations that pass photographs between people and systems. The value is preserving work already done and giving the next person a useful starting point. I want the public project to make that process easy to inspect: a small example, a clear metadata map, a review step and a way to read the result back. My next step is to check how that example moves between tools and document what stays intact. The picture should carry the context we have approved, and the uncertainty we still need to resolve should stay visible.
