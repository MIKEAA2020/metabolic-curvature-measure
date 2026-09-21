// V18 JTB-alignment round: Highlights file (Journal of Theoretical
// Biology requires highlights as a separate editable file with the
// word "highlights" in the file name; 3-5 bullets, each <= 85
// characters including spaces, featuring the biological applications
// as well as the theoretical advancements).
// Output: download/highlights_jtb.docx
const {
  Document, Packer, Paragraph, TextRun, Footer, PageNumber,
  AlignmentType, HeadingLevel,
} = require("docx");
const fs = require("fs");

const TITLE = "Highlights";
const MS_TITLE = "A Geometric Theory of Metabolic Flux Rerouting: How " +
  "Active-Set Curvature Predicts Transcriptional Regulation and " +
  "Protein-Layer Buffering";

const BULLETS = [
  "A discrete curvature measure locates metabolic rerouting at active-set walls",
  "Gene-level metric predicts E. coli transcriptional induction (r = 0.395)",
  "Induced genes sit in operons of CRP-led carbon and energy regulons",
  "Rerouting mass concentrates on fork metabolites of central carbon metabolism",
  "Protein synthesis is buffered; metabolic memory is post-translational",
];

// Hard gate: JTB cap of 85 characters per bullet, 3-5 bullets.
BULLETS.forEach((b) => {
  if (b.length > 85) throw new Error(`Bullet exceeds 85 chars (${b.length}): ${b}`);
});
if (BULLETS.length < 3 || BULLETS.length > 5) {
  throw new Error(`Bullet count ${BULLETS.length} outside 3-5`);
}
console.log("bullet lengths:", BULLETS.map((b) => b.length).join(", "));

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: { ascii: "Times New Roman" }, size: 24, color: "000000" },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: { ascii: "Times New Roman" }, size: 32, bold: true, color: "000000" },
        paragraph: { spacing: { before: 0, after: 160, line: 312 } },
      },
    },
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1417, bottom: 1417, left: 1701, right: 1417 },
        },
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })],
            }),
          ],
        }),
      },
      children: [
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun({ text: TITLE, bold: true })],
        }),
        new Paragraph({
          alignment: AlignmentType.LEFT,
          spacing: { after: 240, line: 312 },
          children: [
            new TextRun({ text: "Manuscript: ", bold: true, italics: false, size: 22 }),
            new TextRun({ text: MS_TITLE, italics: true, size: 22 }),
          ],
        }),
        ...BULLETS.map((b) =>
          new Paragraph({
            bullet: { level: 0 },
            alignment: AlignmentType.LEFT,
            spacing: { after: 120, line: 312 },
            children: [new TextRun({ text: b, size: 24 })],
          })
        ),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(
    "/home/z/my-project/metabolic-curvature-measure/download/highlights_jtb.docx",
    buf
  );
  console.log("highlights_jtb.docx written");
});
