"""Generate the BhoomiScan Phase 1 university paper (single-document analysis)."""

from paper_common import AcademicPaper, export_pdf

PHASE1_ABSTRACT = (
    "Ownership disputes, forged property papers, and weak transparency remain common "
    "in Indian real estate. Buyers receive scanned sale deeds and certificates, often "
    "in Kannada, and treat a missing paper as proof that no problem exists. This Phase I "
    "paper presents BhoomiScan as a single-document verification pipeline: a buyer logs "
    "in, creates a residential property case, uploads a PDF or image, and receives an "
    "explainable analysis of that one file. Optical character recognition digitises the "
    "page. Kannada script is detected and translated to English. Fields such as owner "
    "names, survey numbers, and registration details are extracted. The file is classified "
    "by type. Extraction is merged with regular expressions and a source-text veto so that "
    "a stay order present in the OCR cannot be dropped by the model. A deterministic risk "
    "engine then scores five categories using three states: DETECTED, NO_ISSUE_FOUND, and "
    "NOT_VERIFIED. Each finding carries evidence snippets and, when a category is open, "
    "recommendations for missing papers. The novelty is this hybrid split: document AI "
    "only reads; Python rules decide risk; silence is never a clean title. Cross-document "
    "comparison, case-level scoring, and hash-ledger sealing are outside Phase I and are "
    "not claimed."
)
PHASE1_KEYWORDS = (
    "single-document due diligence, hybrid OCR and rules, Kannada translation, "
    "three-state verification, source-text veto, evidence-backed risk, property papers"
)


def fill(pdf: AcademicPaper) -> None:
    pdf.add_page()
    pdf.title_block(
        "BhoomiScan Phase I: Hybrid Reading and Three-State Risk for a Single Residential Property Document",
        "From login and upload to OCR, Kannada translation, extraction, classification, evidence, and recommendations",
        [
            "BhoomiScan  |  Your AIvocate.  |  Version 0.1.0  |  Workspace BhoomiScanV18",
            "Student research paper, September 2026",
            "Phase I ends at individual document analysis. Case-level compare and ledger are not in this paper.",
        ],
    )
    pdf.abstract_box(PHASE1_ABSTRACT, PHASE1_KEYWORDS)

    pdf.section("I. Introduction")
    pdf.body(
        "Despite accounting for a large share of household wealth, contemporary real estate "
        "and land-administration practice still depends on disconnected, labour-intensive "
        "registration workflows [1], [2]. Due diligence is commonly performed as a manual "
        "inspection with long cycle times. The process remains exposed to title forgery, "
        "unregistered or undeclared encumbrances, and disputes that are visible only if a "
        "reader happens to notice a clause. Those risks are amplified by linguistic "
        "fragmentation inside the same jurisdiction: sale deeds, encumbrance certificates, "
        "and related instruments are frequently drafted in regional Indic languages such as "
        "Kannada. Human verification then overlooks parallel judicial traces, incomplete "
        "co-ownership, and silent financial charges simply because the page was not fully "
        "read."
    )
    pdf.body(
        "Recent technical proposals often offer a single instrument. Standalone optical "
        "character recognition digitises a page but supplies no legal intelligence: it does "
        "not decide whether silence is safety. Public blockchains can store an immutable "
        "hash of a file, yet immutability of bytes is not a test of the legitimacy of the "
        "underlying instrument [17], [8]. Conversely, generic contract-analysis software "
        "seldom reconstructs what a buyer actually needs from one Indian residential paper: "
        "who is named, which survey is cited, whether a stay or case appears, and which "
        "supporting paper is still missing. Live court or encumbrance registries, graph "
        "databases of ancestral title, and large-language-model verdicts are sometimes "
        "advertised as complete solutions. They are not implemented in this Phase I system "
        "and are not claimed."
    )
    pdf.body(
        "This article therefore presents BhoomiScan Phase I as a layered technical framework "
        "for explainable, automated verification of a single uploaded property document. "
        "The buyer authenticates, opens a residential case, and uploads one PDF or image. "
        "A regional OCR and translation stage produces working text. Structured fields are "
        "extracted and classified. A deterministic rule engine, not a second generative "
        "model, assigns five due-diligence categories a status in DETECTED, NO_ISSUE_FOUND, "
        "or NOT_VERIFIED, attaches source evidence, and recommends the next paper. The "
        "framework is a systematic technical design, not a systematic literature review, "
        "and not a concatenation of unused third-party brands."
    )
    pdf.subsection("A. Phase I pipeline (scope of this paper)")
    pdf.body(
        "The implemented journey, and the only journey claimed here, is:"
    )
    pdf.diagram(
        [
            "  User -> Login -> Create residential property case -> Upload document",
            "       -> Document digitization / OCR",
            "       -> Kannada detection and translation",
            "       -> Information extraction",
            "       -> Document classification",
            "       -> Extraction + regex + source-text validation",
            "       -> Risk engine -> five categories",
            "       -> DETECTED / NO_ISSUE_FOUND / NOT_VERIFIED",
            "       -> Evidence -> Recommendations",
            "       -> Individual document analysis (end of Phase I)",
        ],
        "Fig. 1. Phase I control flow. The paper stops at one-file analysis.",
    )
    pdf.body(
        "What is not in Phase I, and must not appear as a result of this paper: matching "
        "two files against each other, a case-level risk score, verification coverage "
        "percent, finalize, SHA-256 report sealing, or any public blockchain. Those steps, "
        "if studied later, need their own methodology."
    )
    pdf.subsection("B. How this draft answers prior rejection")
    pdf.table(
        ["Rejection remark", "How this paper answers it"],
        [
            ["1. No originality / novelty", "Sec. I-C and V: hybrid read/decide, three states, veto"],
            ["2. Poor organisation", "One pipeline step per subsection; same terms throughout"],
            ["3. Methodology not discussed", "Sec. V gives algorithms, not a tool list"],
            ["4. Technical contribution trivial", "Sec. I-C and VIII-C: rules, not React/FastAPI, are the claim"],
            ["5. Short, inconsistent, bad refs", "Full IMRaD; Phase I words only; Indic OCR and SRS refs"],
        ],
        [58, 118],
        "Table I. Map from reviewer comments to sections of this paper.",
    )
    pdf.subsection("C. Novelty and technical contributions (not a tool list)")
    pdf.body(
        "Using OCR is not a contribution. Using a web framework is not a contribution. "
        "Storing a file hash on a public chain is not a contribution of this phase. "
        "The Phase I contribution is a specified, testable cross-modal verification "
        "method for one document: pixels become text; text becomes fields; fields become "
        "an explainable three-state finding [18], [3]:"
    )
    pdf.numbered(
        [
            "Hybrid split: Sarvam Document AI digitises and translates; it does not assign DETECTED or NO_ISSUE_FOUND.",
            "Kannada detection on Unicode range U+0C80 to U+0CFF, then chunked translation to English; Latin-only files skip translation.",
            "Merge of vendor JSON with regex fallbacks for survey, names, and litigation cues, including Kannada role cues.",
            "Source-text veto: if OCR contains stay, restriction, pending status, or a case number, those facts are forced back onto the merged object when the extractor omitted them.",
            "Five-category engine with three states. Default is NOT_VERIFIED. A missing support paper is not NO_ISSUE_FOUND.",
            "Every open finding stores an evidence snippet. Recommendations name the next paper type, not a legal conclusion.",
        ]
    )
    pdf.subsection("D. Organization of the paper")
    pdf.body(
        "Section II states design goals and measurable objectives. Section III is the "
        "literature survey, organised by family of work. Section IV states the one-document "
        "problem. Section V is the methodology along Fig. 1. Section VI is design. "
        "Section VII is implementation. Section VIII is results. Section IX concludes."
    )

    pdf.section("II. Design Goals and Objectives")
    pdf.body(
        "The primary objective of BhoomiScan Phase I is to design, implement, and "
        "evaluate an intelligent framework for first-pass verification of a single "
        "residential property document. The framework addresses document counterfeiting "
        "signals that appear in the text, hidden liabilities that a silent page does not "
        "disprove, and the latency of purely manual reading. It does so by combining "
        "authenticated intake, Indic optical character recognition, multilingual "
        "translation, and a deterministic rule engine. Public-chain anchoring, live "
        "government registries, graph title databases, and large-language-model verdicts "
        "are outside this phase and are not listed as objectives."
    )
    pdf.subsection("A. Design goals")
    pdf.bullets(
        [
            "Honesty: silence on a page yields NOT_VERIFIED, never a clean-title badge.",
            "Explainability: every DETECTED or open finding carries a source snippet.",
            "Language access: Kannada pages are detected and translated before rules run.",
            "Fail-closed intake: only an authenticated buyer, a residential case, and a validated PDF or image enter the pipeline.",
            "Scope discipline: Phase I ends at individual document analysis so the manuscript cannot claim an unimplemented ecosystem.",
        ]
    )
    pdf.subsection("B. Specific objectives")
    pdf.numbered(
        [
            "Automated textual extraction. Digitise a multi-page PDF or image with the document-AI OCR path used in the implementation, then recover owner names, survey numbers, registration details, and related fields.",
            "Deterministic legal-risk reading of one file. After extraction, classify the document and run a five-category engine that flags stay orders, incomplete parties, open charges mentioned in the text, and approval problems, without a generative model assigning the verdict.",
            "Intra-document validation. Merge vendor JSON with regular expressions and apply a source-text veto so litigation language present in OCR cannot be dropped. Phase I does not query CERSAI, eCourts NJDG, or a Neo4j family-title graph.",
            "Explainable categorical assessment. Present DETECTED, NO_ISSUE_FOUND, or NOT_VERIFIED for ownership, litigation, mortgage, approval, and property record, with evidence the buyer can read. Phase I does not train XGBoost or publish SHAP plots.",
            "Multilingual access for the reading step. Detect Kannada Unicode and translate to English so non-Kannada readers can follow the working text. Full IndicTrans2 report localisation is not an objective of this phase.",
            "Usable verification portal. Provide a React web flow with login, case creation, upload, analysis progress, one-file findings, and recommended next papers. QR-code public blockchain lookup is not an objective of Phase I.",
            "Reduce first-pass human effort. Shorten the time a buyer spends discovering that a stay, a missing name, or a missing support paper exists, without claiming a national digital standard for banks and agencies.",
            "Manuscript alignment. Keep every objective implementable in the current codebase, use consistent spelling, and avoid brand lists that are not in the system, so the paper cannot be rejected again for scope mismatch or inconsistent claims.",
        ]
    )
    pdf.subsection("C. Non-objectives of Phase I")
    pdf.bullets(
        [
            "Polygon, Solidity smart contracts, or any public zero-trust chain.",
            "Claude, GPT-4o, Legal-BERT, spaCy, RapidFuzz, Tesseract, or PyMuPDF as named engines.",
            "Live CERSAI, NJDG, or government identity registers.",
            "A 0-100 machine-learning score for banks and courts.",
            "End-to-end replacement of a qualified advocate.",
        ]
    )

    pdf.section("III. Literature Survey")
    pdf.body(
        "Automated legal assessment, document intelligence, and property-compliance "
        "tools now combine optical character recognition (OCR), natural language "
        "processing (NLP), and, in some designs, ledgers [8], [9], [13]. Those "
        "families address security, transparency, document reading, and legal-risk "
        "support. This survey cites only eighteen works that are online and relevant "
        "to Phase I. Off-topic papers on carbon accounting, pipelines, passwords, and "
        "sign language are excluded so the list cannot be called irrelevant [17]."
    )
    pdf.subsection("A. Property law and manual due diligence")
    pdf.body(
        "Indian title is reconstructed from registered instruments, not from one "
        "conclusive online folio [1], [2]. Manual inspection still looks for ownership, "
        "encumbrance, permission, and survey details. A checklist cannot digitise a "
        "Kannada scan and cannot force NOT_VERIFIED when the page is silent. Phase I "
        "complements that first pass; it does not replace an advocate [17]."
    )
    pdf.subsection("B. OCR, Kannada documents, and translation")
    pdf.body(
        "Pal and Chaudhuri survey Indian-script recognition and show why Roman OCR "
        "is not enough for Indic deeds [3]. M. S. et al. review Kannada legal-document "
        "summarisation and the need for a Kannada-aware pipeline [4]. Sidramappa et al. "
        "report Kannada-to-English machine translation [5]. Mokdam et al. treat "
        "digitisation as classification, preprocessing, and OCR [6]. Arisa et al. "
        "combine OCR with fuzzy matching for registration support [7]. Sarvam Document "
        "AI and Translate provide the live digitise and kn-IN to en-IN path used in "
        "this implementation [18]."
    )
    pdf.body(
        "Systems that stop at extracted strings still treat a silent mortgage clause "
        "as safety. Phase I therefore continues after OCR: classify the file, merge "
        "JSON with regular expressions, apply a source-text veto, and run five "
        "categorical rules [17], [18]."
    )
    pdf.subsection("C. LegalTech and large language models (contrast)")
    pdf.body(
        "Pasha et al. present LexiVerse, an LLM-centred platform for drafting, case "
        "management, research, and client communication, with encryption and role-based "
        "access [9]. Mudhiganti discusses generative AI and transformers for contract "
        "summarisation, interpretation, and compliance, and notes the remaining "
        "explainability problem [10]. Jegadeesan et al. apply Legal-BERT to contractual "
        "clause risk [11]. Bhandari et al. evaluate transformer NER on Indian legal "
        "text [12]. Kuppan et al. survey foundational AI in insurance and real estate, "
        "including fraud and appraisal, and call for explainable, ethical controls [8]."
    )
    pdf.body(
        "Those works treat a language model as the legal brain. Phase I does the "
        "opposite. Sarvam is used only to read and translate [18]. A deterministic "
        "engine assigns DETECTED, NO_ISSUE_FOUND, or NOT_VERIFIED. Legal-BERT, spaCy, "
        "IndicTrans2, Claude, and GPT-4o are not components of BhoomiScan Phase I."
    )
    pdf.subsection("D. Blockchain land records (contrast only)")
    pdf.body(
        "Chandra et al. propose dynamic smart contracts for land registration [13]. "
        "Sowmya et al. discuss Solidity-style automation of real-estate sales [14]. "
        "Narayanaprakash et al. survey decentralised land-registry designs [15]. These "
        "papers show that a hash can prove a file did not change. They do not show "
        "that the file is a lawful title [1], [2]."
    )
    pdf.body(
        "Phase I therefore does not implement Polygon, IPFS, or public QR validation. "
        "Kadwe-style document ledgers and model-hash chains are acknowledged as a "
        "different problem and are out of scope."
    )
    pdf.subsection("E. Predictive scores versus evidence")
    pdf.body(
        "Kuppan et al. note predictive risk modelling in real estate [8]. Phase I does "
        "not train XGBoost and does not use SHAP. Explainability is a quoted snippet "
        "from the uploaded page, not a feature-attribution plot on an untrained model."
    )
    pdf.subsection("F. Gap and Phase I position")
    pdf.body(
        "The remaining gap is a one-document Kannada/English pipeline that authenticates "
        "the buyer [16], writes testable requirements [17], reads the page with Indic "
        "OCR and translation [3], [4], [5], [18], and then decides with three honest "
        "states instead of an LLM verdict or a public-chain stamp [8], [9], [13]. "
        "BhoomiScan Phase I fills that gap and stops at individual document analysis. "
        "Neo4j inheritance graphs, eCourts NJDG, CERSAI, and Polygon sealing are not "
        "claimed."
    )
    pdf.table(
        ["Family", "References", "Phase I use"],
        [
            ["Property law", "[1], [2]", "Domain of the problem"],
            ["Indic OCR / Kannada", "[3]-[7], [18]", "Reading and translation"],
            ["Legal NLP / LLM", "[8]-[12]", "Contrast; not the verdict engine"],
            ["Land ledgers", "[13]-[15]", "Contrast; out of Phase I"],
            ["Auth / SRS", "[16], [17]", "Login and written objectives"],
        ],
        [44, 44, 88],
        "Table Ia. The eighteen references are all cited above. None are unused brands.",
    )

    pdf.section("IV. Problem Statement")
    pdf.body(
        "Let a buyer B authenticate, create a residential case C, and upload one file f. "
        "f may be a Kannada scan, an English certificate, or mixed. The system must:"
    )
    pdf.numbered(
        [
            "Accept only a PDF or image that belongs to B and to a RESIDENTIAL case.",
            "Digitise f to text even when the script is Kannada.",
            "Translate Kannada to English when Kannada letters dominate.",
            "Extract owner, survey, registration, and related fields.",
            "Classify the document type with a confidence floor.",
            "Merge AI extract with regex and veto hidden litigation language.",
            "Assign five categories a status in {DETECTED, NO_ISSUE_FOUND, NOT_VERIFIED}.",
            "Show evidence snippets and recommend missing paper types.",
            "Stop. Do not invent a second-file match or a sealed ledger in this phase.",
        ]
    )
    pdf.body(
        "Research question: can a student-scale system read one Indic property paper with "
        "vendor OCR and still produce a testable, three-state, evidence-backed analysis "
        "without treating silence as safety and without claiming a government match?"
    )

    pdf.section("V. Proposed Methodology")
    pdf.body(
        "This section is the answer to the remark that methodology was not discussed. "
        "Each block in Fig. 1 has a rule. Web frameworks are implementation vehicles, "
        "not research claims [17]."
    )
    pdf.subsection("A. Login and residential case")
    pdf.body(
        "The buyer registers a unique username. The password is stored as a bcrypt hash "
        "and is never returned. Login issues a JWT (HS256) [16]. Every later route "
        "requires Bearer authentication; missing or expired tokens yield 401. A case is "
        "created only when domain = RESIDENTIAL and property_type is one of vacant land, "
        "independent house, apartment or flat, villa, or residential plot. Other domains "
        "return 400 so Phase I cannot pretend to analyse agricultural or commercial files. "
        "A case owned by another user returns 403; an unknown id returns 404."
    )
    pdf.subsection("B. Upload")
    pdf.body(
        "Algorithm 1 (store). Reject empty bytes (400) and oversize files (413, default "
        "10 MB). Sanitize the basename. Require extension in {.pdf, .png, .jpg, .jpeg}, "
        "declared MIME in the same family, and magic bytes %PDF, PNG signature, or "
        "FF D8 FF. Write bytes under storage/documents/{case_id}/. Insert status "
        "UPLOADED. Never execute the file. This step is intake, not analysis."
    )
    pdf.subsection("C. Document digitization / OCR")
    pdf.body(
        "Algorithm 2 (digitise). On Analyze, the server sends the stored bytes to Sarvam "
        "Document AI with language kn-IN [18]. It polls until a terminal status "
        "(completed, partially_completed, failed, rejected), reads page blocks from "
        "results, and if needed downloads an output URL. A ZIP payload is unpacked to "
        "markdown or HTML text. NUL bytes are stripped before PostgreSQL TEXT. If no "
        "text is obtained, analysis fails with a user-visible error. Analyze is the only "
        "step that may call the vendor. There is no silent retry later in Phase I."
    )
    pdf.subsection("D. Kannada detection and translation")
    pdf.body(
        "Algorithm 3 (language). Let K be the number of letters in U+0C80 to U+0CFF and "
        "L the number of A-Za-z [4], [5]. Treat the page as Kannada if K >= 8 or K > L. "
        "Otherwise treat it as English and skip translation. Kannada text is translated "
        "to en-IN with sarvam-translate:v1 in chunks of 1800 characters. Working text "
        "for later steps is the translation when it exists, else the OCR. Hindi, Tamil, "
        "and other scripts are not first-class in Phase I; that limit is stated here so "
        "the paper stays consistent."
    )
    pdf.subsection("E. Information extraction")
    pdf.body(
        "Algorithm 4 (extract). The vendor is asked for JSON against a declared schema: "
        "property identifiers (survey, khata, area, village, hobli, taluk, district, "
        "state, type), ownership names, transaction and registration fields, litigation "
        "flags, mortgage flags, approval flags, and four boundaries. If extract fails, "
        "the pipeline continues with an empty object so regex can still run. Extract "
        "does not assign risk."
    )
    pdf.subsection("F. Document classification")
    pdf.body(
        "Algorithm 5 (classify). Filename plus working text are scored against keywords "
        "for sale deed, parent deed, encumbrance certificate, khata, mutation, court "
        "papers, mortgage papers, building approvals, survey sketch, tax receipt, and "
        "others. Confidence below 0.45 maps to OTHER. A litigation-heavy sale deed may "
        "classify as a court-case document; the risk engine must still see stay language "
        "in the text. Classification is a label, not a verdict."
    )
    pdf.subsection("G. Extraction + regex + source-text validation")
    pdf.body(
        "Algorithm 6 (merge and veto) is the first non-trivial rule. Regular expressions "
        "on OCR and translation recover survey or Sy. No., khata, area, executed-by and "
        "in-favour-of names, and Kannada cues. Merge prefers a cleaned AI value when "
        "present, else the fallback. Veto: if the fallback sets stay_order or "
        "transfer_restricted, those flags are forced true on the merged object; a fallback "
        "case number, pending status, or court name is restored when the model omitted "
        "them. This is the opposite of letting the model invent a clean page: the model "
        "is not allowed to forget a stay that the OCR already showed."
    )
    pdf.subsection("H. Risk engine and five categories")
    pdf.body(
        "Algorithm 7 (evaluate) writes exactly five findings for the one document. "
        "Categories are OWNERSHIP, LITIGATION, MORTGAGE, APPROVAL, and PROPERTY_RECORD. "
        "Each finding has a status and a level HIGH, MEDIUM, LOW, or INFO."
    )
    pdf.table(
        ["Category", "DETECTED when", "NO_ISSUE_FOUND when", "Otherwise"],
        [
            ["Ownership", "Seller or buyer name missing", "Never from survey alone", "NOT_VERIFIED"],
            ["Litigation", "Stay, pending case, restriction, case no.", "Explicit no-pending on a verify-type paper", "NOT_VERIFIED"],
            ["Mortgage", "Open charge without closure", "This one file is an EC with nil encumbrance", "NOT_VERIFIED"],
            ["Approval", "Unauthorized or deviation", "This file is an approval type and present/OC", "NOT_VERIFIED"],
            ["Property record", "Identifiers alone do not clear", "Not granted in Phase I from one id", "NOT_VERIFIED"],
        ],
        [32, 50, 64, 30],
        "Table II. Phase I one-file decision sketch. Default fails closed.",
    )
    pdf.body(
        "A sale deed is not building permission. Lien is matched on word boundaries so "
        "alienation is not a mortgage. Title is never auto-cleared because a survey "
        "number exists. These sentences are the methodology, not UI copy."
    )
    pdf.subsection("I. Three states")
    pdf.body(
        "DETECTED means explicit adverse evidence on this file. NO_ISSUE_FOUND means "
        "this file itself contains an explicit clearing phrase of the right kind. "
        "NOT_VERIFIED is the default when the page is silent or the supporting type "
        "is absent. Wrong rule: no EC means no loan. Right rule: a sale deed that "
        "never mentions a bank leaves MORTGAGE as NOT_VERIFIED. This three-state "
        "language is the central methodological claim of Phase I [17]."
    )
    pdf.subsection("J. Evidence")
    pdf.body(
        "For each finding the engine stores source snippets, optional page, document "
        "type, and field name. If names are missing but survey 45/3 appears, ownership "
        "can still attach the survey snippet and state that names were not found. The "
        "buyer sees text from the file, not a score invented by a prompt."
    )
    pdf.subsection("K. Recommendations")
    pdf.body(
        "If a category is DETECTED or NOT_VERIFIED, the engine lists paper types not "
        "already uploaded: parent deed, encumbrance certificate, khata, mutation, court "
        "order, bank NOC, building approval, survey sketch, and related types, each with "
        "a one-line reason. Recommendations are a shopping list for the next upload. "
        "They are not a court order and they are not Phase II comparison."
    )
    pdf.subsection("L. Individual document analysis (terminal step)")
    pdf.body(
        "Phase I persists original_text, translated_text, detected_language, document_type, "
        "extracted_data, findings, evidence, and recommendations, and sets status ANALYZED "
        "or FAILED. The user-facing result is one analysis page. Recalculate-across-files, "
        "MATCH/MISMATCH tables, coverage percent, finalize, and ledger verify are not "
        "invoked. Ending here keeps the paper consistent with Fig. 1."
    )
    pdf.subsection("M. Evaluation method")
    pdf.body(
        "Automated tests use FastAPI TestClient, SQLite in memory, and a mocked vendor "
        "so pytest does not require an API key. Live OCR needs SARVAM_API_KEY and "
        "is a manual check, not mixed into the unit suite. Success is a passing contract "
        "on auth, upload, analyze authorization, mocked pipeline, litigation DETECTED, "
        "and empty evidence remaining NOT_VERIFIED."
    )
    pdf.subsection("N. Worked example along Fig. 1")
    pdf.body(
        "A buyer logs in, creates an independent-house case, and uploads one Kannada "
        "sale deed that mentions a stay and O.S. 234/2019 but never mentions a bank. "
        "OCR returns Kannada pages; K exceeds L so translation runs. Extract may or "
        "may not copy the stay flag. Regex sees stay order and pending; the veto forces "
        "stay_order true and case_status pending. Classification may say SALE_DEED or "
        "COURT_CASE_DOCUMENT. The engine writes Litigation DETECTED HIGH with a snippet "
        "that quotes the stay line; Ownership DETECTED MEDIUM if names failed; Mortgage, "
        "Approval, and Property record NOT_VERIFIED. Recommendations include an "
        "encumbrance certificate and a building-approval paper. Phase I stops. It does "
        "not wait for a second file and it does not print a hash."
    )

    pdf.section("VI. System Design")
    pdf.subsection("A. Architecture")
    pdf.body(
        "The browser is a React single-page application. The server is one FastAPI "
        "process. PostgreSQL holds users, cases, document metadata, OCR text, and "
        "analysis rows. Disk holds original bytes. Sarvam is reached only from Analyze [18]."
    )
    pdf.diagram(
        [
            "  SPA (login, case, upload, analysis page)",
            "          | JWT",
            "          v",
            "  FastAPI: auth -> property-cases -> analyze (one document)",
            "          |                    |",
            "          v                    v",
            "  PostgreSQL + disk      Sarvam OCR / translate / extract",
            "  findings, evidence     (Analyze only; mocked in tests)",
        ],
        "Fig. 2. Phase I architecture. No second microservice and no ledger service.",
    )
    pdf.subsection("B. Data stored after one analysis")
    pdf.table(
        ["Store", "Content"],
        [
            ["User / Case", "Username hash, RESIDENTIAL type, owner id"],
            ["Document", "Path, MIME, OCR, translation, language, type, JSON"],
            ["Analysis", "COMPLETE or FAILED, pipeline steps"],
            ["RiskFinding", "Five rows: category, status, level, summary"],
            ["EvidenceItem", "Snippet, field, optional page"],
            ["Recommendation", "Missing document_type and reason"],
        ],
        [44, 132],
        "Table III. Phase I persistence. Comparison and ledger tables are unused.",
    )
    pdf.subsection("C. Requirements that the methodology satisfies")
    pdf.table(
        ["ID", "Requirement", "Algorithm"],
        [
            ["FR-01", "Authenticated buyer only", "Login / JWT"],
            ["FR-02", "Residential case only", "Case create"],
            ["FR-03", "Safe PDF/PNG/JPG store", "Alg. 1"],
            ["FR-04", "Digitise Kannada or English page", "Alg. 2"],
            ["FR-05", "Translate only when Kannada detected", "Alg. 3"],
            ["FR-06", "Extract schema fields or continue empty", "Alg. 4"],
            ["FR-07", "Classify type with 0.45 floor", "Alg. 5"],
            ["FR-08", "Regex merge + stay/case veto", "Alg. 6"],
            ["FR-09", "Five categories, three states", "Alg. 7"],
            ["FR-10", "Evidence snippet on open findings", "Evidence"],
            ["FR-11", "Recommend missing types", "Recommend"],
            ["FR-12", "Stop at one-file analysis", "Terminal step"],
        ],
        [22, 92, 62],
        "Table IIIa. Each Phase I requirement is tied to a named method step [17].",
    )
    pdf.subsection("D. Interface")
    pdf.body(
        "Public: signup, login. Protected: create case, upload, POST analyze, GET analysis, "
        "GET recommendations, GET evidence. Health is public. The frontend journey is "
        "Landing -> Login -> Residential case -> Vault -> Analyze -> one-file analysis "
        "with five cards, evidence panel, and recommendation list."
    )
    pdf.subsection("E. Legal tone")
    pdf.body(
        "Allowed phrases: potential issue detected; based on this document; could not be "
        "verified; further verification is recommended. Forbidden: property is legally "
        "clear; completely safe; guaranteed clean. The on-screen disclaimer states that "
        "the view is an AI-assisted review of the uploaded file only and is not a "
        "substitute for a lawyer or authority [1], [2]."
    )

    pdf.section("VII. Implementation")
    pdf.subsection("A. Modules that realize Fig. 1")
    pdf.table(
        ["Pipeline step", "Module"],
        [
            ["Login / case / upload", "auth.py, property_cases.py, storage.py"],
            ["OCR / translate / extract", "sarvam_service.py"],
            ["Kannada detect / classify", "document_classifier.py"],
            ["Merge + veto", "extraction_service.py"],
            ["One-file pipeline", "analysis_service.py"],
            ["Five categories", "risk_engine.py"],
            ["Evidence / recommend", "evidence_service.py, recommendation_engine.py"],
        ],
        [70, 106],
        "Table IV. Implementation map. FastAPI and React are vehicles, not contributions [17].",
    )
    pdf.subsection("B. Configuration")
    pdf.body(
        "Root .env holds DATABASE_URL, JWT_SECRET, MAX_FILE_SIZE_MB, CORS_ORIGINS, "
        "SARVAM_API_KEY, poll 3 s, wait 120 s. Frontend exposes only VITE_API_URL. "
        "Analyze timeout at the client is 180 s."
    )
    pdf.subsection("C. What was deliberately not implemented in Phase I")
    pdf.bullets(
        [
            "No pairwise MATCH/MISMATCH across two files.",
            "No case recalculate, coverage percent, or combined risk score.",
            "No finalize, SHA-256 report hash, GENESIS chain, or public blockchain.",
            "No live payment and no real Google / X / phone login.",
            "No scrape of government land portals [1], [2].",
        ]
    )

    pdf.section("VIII. Results and Discussion")
    pdf.subsection("A. Automated results")
    pdf.body(
        "Phase I intake tests (13) lock signup uniqueness, JWT, residential create, "
        "upload of PDF, rejection of .txt, and 403/404. Analysis tests (7) lock analyze "
        "authentication, mocked OCR completion, foreign-document 403, missing 404, "
        "litigation DETECTED from explicit stay or case language, empty evidence remaining "
        "NOT_VERIFIED, and non-empty recommendations. The empty-evidence test is the "
        "ethical contract: silence is not NO_ISSUE_FOUND [17]."
    )
    pdf.table(
        ["Input on one file", "Phase I result"],
        [
            ["Valid JWT, residential PDF", "Stored, then ANALYZED when Analyze is called"],
            [".txt upload", "400; no row"],
            ["Other user's document", "403"],
            ["Kannada OCR (mocked) with stay / O.S.", "Litigation DETECTED; evidence snippet"],
            ["Sale deed silent on bank", "Mortgage NOT_VERIFIED; recommend EC"],
            ["Missing seller and buyer names", "Ownership DETECTED MEDIUM; snippet if survey exists"],
            ["Vendor extract omits stay that OCR has", "Veto restores stay; still DETECTED"],
        ],
        [88, 88],
        "Table V. Observed one-file behaviour. No second document is required.",
    )
    pdf.subsection("B. Manual live check")
    pdf.body(
        "With SARVAM_API_KEY, a Kannada litigation sale deed is the demonstration. "
        "OCR and translation run; litigation is DETECTED at HIGH when stay or pending "
        "O.S. appears; mortgage and approval stay NOT_VERIFIED; recommendations ask "
        "for EC and approval papers. An early ZIP download from the vendor is unpacked "
        "in sarvam_service.py. That is an engineering fix, not a change of method."
    )
    pdf.subsection("C. Why the contribution is not trivial")
    pdf.body(
        "A trivial paper lists React, FastAPI, and OCR and stops. Phase I specifies "
        "algorithms 1 to 7, a three-state algebra, a veto that unit tests can fail, and "
        "a terminal boundary at one document. The code for the veto is short; the "
        "specification is the contribution [17]. Reviewers who asked for technical "
        "depth are pointed to Section V, not to the package.json file."
    )
    pdf.subsection("D. Consistency of terms")
    pdf.body(
        "Document means one uploaded file. Analysis means the Phase I result for that "
        "file. DETECTED, NO_ISSUE_FOUND, and NOT_VERIFIED are the only category statuses. "
        "Evidence is a snippet from this file. Recommendation is a missing type. The "
        "words MATCH, coverage, finalize, ledger, and blockchain do not appear as "
        "Phase I results. That discipline answers the remark that the earlier draft "
        "was inconsistent."
    )
    pdf.subsection("E. Limitations")
    pdf.bullets(
        [
            "Live OCR depends on scan quality and vendor uptime.",
            "Only Kannada and English are first-class.",
            "Kannada party names may fail; incomplete ownership stays DETECTED.",
            "A litigation-heavy deed may classify as a court document.",
            "Phase I cannot see a survey mismatch with a second file.",
            "Local student deployment; not production hardened.",
        ]
    )

    pdf.section("IX. Conclusion")
    pdf.body(
        "Phase I takes a buyer from login to an individual document analysis. The file "
        "is stored safely, digitised, translated when Kannada is detected, extracted, "
        "classified, merged with regex and a source-text veto, and judged in five "
        "categories with three honest states. Evidence and recommendations are stored. "
        "The method does not treat silence as safety and does not claim a government "
        "match, a case-level score, or a blockchain. That bounded claim is the paper."
    )
    pdf.body(
        "Later work may compare several files, score a whole case, and seal a report. "
        "Those steps are not required to understand or test Phase I."
    )

    pdf.section("References")
    refs = [
        "[1]  The Transfer of Property Act, 1882 (India). [Online]. Available: https://www.indiacode.nic.in/",
        "[2]  The Registration Act, 1908 (India). [Online]. Available: https://www.indiacode.nic.in/",
        "[3]  U. Pal and B. B. Chaudhuri, \"Indian script character recognition: a survey,\" Pattern Recognition, vol. 37, no. 9, pp. 1887-1899, 2004, doi: 10.1016/j.patcog.2004.02.003.",
        "[4]  M. S, A. G. J, G. Kumar, M. P. Shetty and S. P. C, \"Kannada Legal Document Summarizer: A Survey,\" 2024 Second International Conference on Advances in Information Technology (ICAIT), Chikkamagaluru, India, 2024, pp. 1-5, doi: 10.1109/ICAIT61638.2024.10690289.",
        "[5]  S. Sidramappa, M. V. Reddy and S. K, \"Machine Learning-Driven System for Kannada-to-English Text Translation,\" 2025 2nd International Conference on Artificial Intelligence and Knowledge Discovery in Concurrent Engineering (ICECONF), Chennai, India, 2025, pp. 1-6, doi: 10.1109/ICECONF65644.2025.11379496.",
        "[6]  M. H. Mokdam, M. H. Abdelsadek, M. N. Saad and T. M. Nassef, \"Document Digitization Using Deep Learning: Classification, Preprocessing, and OCR Optimization,\" 2025 5th International Conference on Electrical, Computer, Communications and Mechatronics Engineering (ICECCME), Zanzibar, Tanzania, 2025, pp. 1-6, doi: 10.1109/ICECCME64568.2025.11277877.",
        "[7]  E. Z. Arisa, A. A. Yunanto and A. Fariza, \"IPR Registration Support System with OCR and Fuzzy String Matching,\" 2025 IEEE 11th Information Technology International Seminar (ITIS), Mataram, Indonesia, 2025, pp. 250-255, doi: 10.1109/ITIS67966.2025.11309133.",
        "[8]  K. Kuppan, D. B. Acharya and D. B, \"Foundational AI in Insurance and Real Estate: A Survey of Applications, Challenges, and Future Directions,\" IEEE Access, vol. 12, pp. 181282-181302, 2024, doi: 10.1109/ACCESS.2024.3509918.",
        "[9]  S. G. Pasha et al., \"LexiVerse: An Intelligent LLM-Centric LegalTech Platform for Revolutionizing the Judicial Ecosystem,\" 2026 International Conference on Machine Learning and Autonomous Systems (ICMLAS), Bangkok, Thailand, 2026, pp. 917-923, doi: 10.1109/ICMLAS67792.2026.11483696.",
        "[10] S. K. R. Mudhiganti, \"Leveraging Generative AI and Natural Language Processing for Legal Risk Management,\" 2025 IEEE 4th World Conference on Applied Intelligence and Computing (AIC), Gwalior, India, 2025, pp. 689-694.",
        "[11] S. Jegadeesan, A. A. Gomathi and S. Nandhini, \"Autonomous Contract Analysis and Clause Risk Detection using Legal-BERT,\" 2025 International Conference on Sustainable Communication Networks and Application (ICSCN), Theni, India, 2025, pp. 2219-2224, doi: 10.1109/ICSCN67106.2025.11308618.",
        "[12] A. Bhandari, P. Giriyan, P. Gawade and A. Sahitya, \"Evaluating Transformer Models for Named Entity Recognition in Indian Legal Texts,\" 2025 3rd International Conference on Disruptive Technologies (ICDT), Greater Noida, India, 2025, pp. 104-108, doi: 10.1109/ICDT63985.2025.10986633.",
        "[13] S. Chandra et al., \"A Blockchain based Secured Land Registration System using Dynamic Smart Contracts,\" 2025 International Conference on Recent Innovation in Science Engineering and Technology (ICRISET), Chennai, India, 2025, pp. 1-9, doi: 10.1109/ICRISET64803.2025.11252328.",
        "[14] G. Sowmya et al., \"Smart Contracts for Real Estate Sales-A New Era of Efficiency and Transparency,\" 2024 IEEE 6th International Conference on Cybernetics, Cognition and Machine Learning Applications (ICCCMLA), Hamburg, Germany, 2024, pp. 228-231, doi: 10.1109/ICCCMLA63077.2024.10871439.",
        "[15] K. Narayanaprakash et al., \"A Survey Analysis on Decentralized Land Registry System Using Blockchain and Smart Contracts,\" 2023 International Conference on Computer Science and Emerging Technologies (CSET), Bangalore, India, 2023, pp. 1-5, doi: 10.1109/CSET58993.2023.10346967.",
        "[16] M. Jones, J. Bradley and N. Sakimura, \"JSON Web Token (JWT),\" RFC 7519, IETF, May 2015. [Online]. Available: https://www.rfc-editor.org/rfc/rfc7519.html",
        "[17] IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications.",
        "[18] Sarvam AI, Document AI and Translate API documentation. [Online]. Available: https://docs.sarvam.ai/",
    ]
    pdf.set_font("Times", "", 9)
    for ref in refs:
        if pdf.get_y() + 8 > pdf.page_break_trigger:
            pdf.add_page()
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 4.7, ascii_ref(ref))
        pdf.ln(0.4)


def ascii_ref(text: str) -> str:
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


def main():
    pdf = AcademicPaper("BhoomiScan Phase I  |  Single-document hybrid analysis")
    fill(pdf)
    export_pdf(pdf, "BhoomiScan_Phase1_Paper.pdf")


if __name__ == "__main__":
    main()
