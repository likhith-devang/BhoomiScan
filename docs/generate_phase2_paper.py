"""Generate the BhoomiScan Phase 2 university paper (analysis + case diligence + local hash)."""

from paper_common import SHARED_ABSTRACT, SHARED_KEYWORDS, AcademicPaper, export_pdf


def fill(pdf: AcademicPaper) -> None:
    pdf.add_page()
    pdf.title_block(
        "BhoomiScan Phase II: Hybrid Indic Document Reading and Deterministic Three-State Risk for Residential Due Diligence",
        "OCR and translation as input; Python rules, cross-document compare, coverage, and a local SHA-256 chain as verdict",
        [
            "BhoomiScan  |  Your AIvocate.  |  Version 0.1.0  |  Workspace BhoomiScanV18",
            "Student research paper, September 2026",
            "Builds on Phase I intake. Does not claim a public blockchain or a legal guarantee.",
        ],
    )
    pdf.abstract_box(SHARED_ABSTRACT, SHARED_KEYWORDS)

    pdf.section("I. Introduction")
    pdf.body(
        "A stored PDF is not a reviewed title. Karnataka residential files are often scanned "
        "Kannada deeds mixed with English certificates [1], [2]. A buyer who cannot read the "
        "script, or who treats a missing encumbrance certificate as good news, is exposed. "
        "Generic chat systems compound the exposure: they can declare a property clear when "
        "the text is silent."
    )
    pdf.body(
        "BhoomiScan Phase II starts from the Phase I vault (JWT user, residential case, "
        "validated bytes on disk) and adds a reading-and-verdict pipeline. The methodological "
        "split is the contribution: a commercial Indic document service is an input device; "
        "verdicts are Python functions that a unit test can freeze [3], [4]."
    )
    pdf.subsection("A. Contributions")
    pdf.numbered(
        [
            "A hybrid pipeline: digitise and translate with Sarvam; classify, merge, score, and compare in Python.",
            "A three-state risk language (DETECTED / NO_ISSUE_FOUND / NOT_VERIFIED) so missing evidence cannot become a green tick.",
            "A source-text veto on stay, restriction, pending status, and case number so extraction JSON cannot hide litigation language present in OCR.",
            "Deterministic cross-document comparison with survey-prefix normalization, name folding, and 2% area tolerance.",
            "Separation of risk score (points only from DETECTED) from verification coverage (five-category completeness).",
            "A local SHA-256 GENESIS chain over canonical report JSON, verified by recomputation, explicitly not a public blockchain.",
        ]
    )
    pdf.subsection("B. What this paper refuses to claim")
    pdf.bullets(
        [
            "That the property is legally clear, safe, or guaranteed.",
            "That the hash chain is Bitcoin, Ethereum, mining, a wallet, or a smart contract.",
            "That government portals are scraped or that payments and OAuth are live.",
            "That an LLM decides MATCH versus MISMATCH.",
        ]
    )
    pdf.subsection("C. Organization")
    pdf.body(
        "Section II places the work against manuals, portals, and opaque AI. Section III "
        "states the problem. Section IV is the methodology (algorithms and formulae). "
        "Section V is design. Section VI is implementation. Section VII is results. "
        "Section VIII concludes."
    )

    pdf.section("II. Related Work")
    pdf.subsection("A. Manual due diligence")
    pdf.body(
        "Advocates already perform the five checks this product names: ownership, litigation, "
        "encumbrance, approval, and survey or khata consistency [1], [2]. Manual work does "
        "not automatically OCR Kannada, does not normalize Sy. No. against Survey No., and "
        "does not leave a recomputed hash of the written opinion. Phase II is a first pass "
        "for a buyer, not a substitute for that professional [5]."
    )
    pdf.subsection("B. Document AI and Indic OCR")
    pdf.body(
        "Optical character recognition for Indian scripts is a long-studied problem [6]. "
        "Vendor document-AI products now wrap OCR, layout, and optional structured extract. "
        "Sarvam is used here as such a vendor [3]. Using a vendor is not the novelty. The "
        "novelty is what is not delegated: status assignment, comparison, scoring, and "
        "integrity. Related extraction work that stops at JSON fields still leaves the "
        "buyer with a silent mortgage when no encumbrance paper was uploaded."
    )
    pdf.subsection("C. Risk scores and checklists")
    pdf.body(
        "Binary safe/unsafe scores hide incompleteness. Software-requirements practice asks "
        "that unspecified behaviour be explicit [7]. Our three-state model is closer to "
        "a requirements checklist than to a credit score: NOT_VERIFIED is a first-class "
        "outcome. Coverage percent is reported separately so a filled vault is not confused "
        "with a low-risk vault."
    )
    pdf.subsection("D. Integrity of reports")
    pdf.body(
        "SHA-256 is the NIST secure hash [8]. Hash chains appear in many audit logs. Public "
        "blockchains add consensus and tokens that this student system does not need and "
        "does not implement. We store previous_hash = GENESIS for the first record and link "
        "later versions by report version, not by wall-clock time, to avoid timezone false "
        "tamper. Related work on trusted timestamping (RFC 3161) is future work, not a claim [9]."
    )
    pdf.subsection("E. Gap")
    pdf.body(
        "No student-scale system we implement here combined Indic reading, a vetoed merge, "
        "three-state categories, pairwise field compare, dual meters (score versus coverage), "
        "and a recomputed local hash, while refusing to call silence safety. That combination "
        "is the Phase II gap."
    )
    pdf.table(
        ["Approach", "Reads Kannada", "Absence rule", "Compare fields", "Integrity"],
        [
            ["Manual checklist", "Human only", "Often implicit", "By eye", "None"],
            ["Vendor OCR alone", "Yes", "Usually none", "No", "None"],
            ["LLM chat over scans", "Maybe", "Can invent clear title", "Unstable", "None"],
            ["Public blockchain stamp", "No", "No", "No", "Consensus tokens"],
            ["BhoomiScan Phase II", "Vendor + rules", "NOT_VERIFIED default", "Deterministic", "Local SHA-256"],
        ],
        [40, 32, 42, 32, 30],
        "Table 0a. Related approaches versus this paper. Public blockchain is a different problem.",
    )

    pdf.section("III. Problem Statement")
    pdf.body(
        "Given a Phase I case C with documents D1..Dk, produce a case-level view that is "
        "explainable and testable. Each Di may be Kannada, English, or mixed. The system "
        "must not conclude NO_ISSUE_FOUND merely because a category was not mentioned. "
        "It must notice when two files disagree on survey, names, area, or boundaries. "
        "It must let the buyer add an encumbrance certificate later without paying for OCR "
        "again. After finalize, a later reader must be able to tell VALID from TAMPERED "
        "without trusting the stored hash blindly."
    )
    pdf.body(
        "Academic question: can Indic document AI plus deterministic rules present five "
        "categories as DETECTED, NOT_VERIFIED, or NO_ISSUE_FOUND with evidence, compare "
        "fields without an LLM, and seal a versioned report with SHA-256, without faking "
        "a public blockchain or a legal guarantee?"
    )

    pdf.section("IV. Proposed Methodology")
    pdf.subsection("A. Hybrid stance")
    pdf.body(
        "Fig. 1 separates I/O from verdict. Sarvam is invoked only on Analyze. Recalculate "
        "reads stored original_text, translated_text, and extracted_data. Tests monkeypatch "
        "digitise, translate, and extract so pytest never bills the vendor [4], [10]."
    )
    pdf.diagram(
        [
            "  [File bytes] --> (Digitise kn-IN) --> original_text",
            "       |                                    |",
            "       +----> (Extract schema JSON)         v",
            "                     |              looks_like_kannada?",
            "                     v                    yes --> (Translate chunks 1800) --> English",
            "              ai_extract                            |",
            "                     |                              v",
            "                     +----> (merge_extraction + veto) --> extracted",
            "                                      |",
            "                                      v",
            "                     classify --> evaluate_risks --> evidence --> recommend",
            "                                      |",
            "                     +-- Recalculate: merge statuses, compare, score, coverage",
            "                     +-- Finalize: canonical JSON, SHA-256, GENESIS chain",
        ],
        "Fig. 1. Phase II control flow. The LLM path, if any inside the vendor, does not assign risk status.",
    )
    pdf.subsection("B. Language detection and translation")
    pdf.body(
        "Digitise is requested with language kn-IN because the target corpus is Karnataka "
        "residential paper. After OCR, let K be the count of Unicode letters in U+0C80 to "
        "U+0CFF and L the count of A-Za-z. The document is treated as Kannada if K >= 8 or "
        "K > L [6]. Kannada text is translated to en-IN with model sarvam-translate:v1 in "
        "chunks of 1800 characters. English-only files skip translation. Other Indian "
        "languages are not first-class in this phase; that limitation is stated, not hidden."
    )
    pdf.subsection("C. Classification")
    pdf.body(
        "A keyword scorer on filename plus working text chooses among sale deed, parent deed, "
        "encumbrance certificate, khata, mutation, court papers, mortgage papers, building "
        "approvals, survey sketch, tax receipt, and others. Confidence below 0.45 maps to "
        "OTHER. A litigation-heavy sale deed may classify as a court-case document; tests "
        "and the interface must still show litigation if the text contains it."
    )
    pdf.subsection("D. Extraction merge and source-text veto")
    pdf.body(
        "The extract schema groups property identifiers, ownership names, transaction "
        "fields, litigation, mortgage, approval, and four boundaries. Regular expressions "
        "supply fallbacks (survey/sy no, khata, area, executed-by / in-favour-of names, "
        "Kannada cues). Merge prefers a cleaned AI value when present, else the fallback. "
        "Veto (Algorithm 2): if fallback sees stay_order or transfer_restricted, those flags "
        "are forced true on the merged object; if fallback has a case number or pending "
        "status, they are restored when the model omitted them. This is the anti-hallucination "
        "rule in the opposite direction: the model is not allowed to forget a stay."
    )
    pdf.subsection("E. Three-state risk (Algorithm 3)")
    pdf.body(
        "Categories are OWNERSHIP, LITIGATION, MORTGAGE, APPROVAL, PROPERTY_RECORD. "
        "Each receives one status and a level HIGH, MEDIUM, LOW, or INFO."
    )
    pdf.bullets(
        [
            "DETECTED: explicit adverse evidence (incomplete seller/buyer names; pending case, stay, restriction; open charge without closure; unauthorized construction; later overlay of a high-severity mismatch).",
            "NO_ISSUE_FOUND: a relevant document explicitly clears the category (example: encumbrance certificate with nil / no / free from encumbrance).",
            "NOT_VERIFIED: default when papers are missing or silent. No EC means mortgage NOT_VERIFIED, never NO_ISSUE_FOUND.",
        ]
    )
    pdf.body(
        "Ownership is never auto-cleared from a survey number alone. A sale deed is not "
        "building permission. Lien matches on word boundaries so alienation is not a mortgage. "
        "Case merge: DETECTED wins; else any NO_ISSUE_FOUND; else NOT_VERIFIED; then MISMATCH "
        "overlays DETECTED on the affected category."
    )
    pdf.table(
        ["Category", "Typical DETECTED trigger", "Typical NO_ISSUE_FOUND", "Default"],
        [
            ["Ownership", "Missing seller or buyer name", "Never auto-cleared by survey only", "NOT_VERIFIED"],
            ["Litigation", "Stay, pending O.S., restriction", "Explicit no pending on a verify-type paper", "NOT_VERIFIED"],
            ["Mortgage", "Open charge without closure", "EC with nil / free from encumbrance", "NOT_VERIFIED"],
            ["Approval", "Unauthorized or deviation", "Approval paper plus present or OC", "NOT_VERIFIED"],
            ["Property record", "Later MISMATCH on survey or bounds", "Not granted from one identifier", "NOT_VERIFIED"],
        ],
        [32, 52, 62, 30],
        "Table 0. Decision sketch for Algorithm 3. Defaults fail closed.",
    )
    pdf.subsection("F. Comparison (Algorithm 4)")
    pdf.body(
        "Fields compared include seller, buyer, owner, survey, khata, area, village, hobli, "
        "taluk, district, property type, north/south/east/west, registration number and date, "
        "and previous deed number. Normalization strips prefixes (Survey No., Sy. No., Khata "
        "No.). Names collapse whitespace and case. Area converts square metres to square feet "
        "by 10.7639 and allows 2% relative tolerance. If fewer than two documents carry a "
        "value, the result is NOT_AVAILABLE; otherwise MATCH or MISMATCH with severity and "
        "a plain-language explanation. No language model is consulted."
    )
    pdf.subsection("G. Score and coverage formulae")
    pdf.body(
        "Let F be the set of findings after merge. Risk score uses only DETECTED rows:"
    )
    pdf.equation("score = min(100,  70*|HIGH| + 15*|MEDIUM| + 10*|LOW|)")
    pdf.body(
        "Overall level is HIGH if any DETECTED HIGH exists or score >= 40; MEDIUM if any "
        "DETECTED MEDIUM exists or score >= 10; otherwise LOW. NOT_VERIFIED adds zero points."
    )
    pdf.body(
        "Coverage walks the five categories. Verified (DETECTED or NO_ISSUE_FOUND) weights 1.0. "
        "Partially Verified (NOT_VERIFIED but a related paper type was uploaded) weights 0.5. "
        "Not Verified weights 0.0."
    )
    pdf.equation("coverage% = round(100 * (sum of five weights) / 5)")
    pdf.body(
        "An empty vault can have score 0 (LOW) and coverage 0%. That pair is intentional: "
        "low score is not safety; it may mean nothing was checked [7]."
    )
    pdf.subsection("H. Evidence and recommendations")
    pdf.body(
        "Each finding may store source snippets, page, document type, and field name. "
        "Recommendations list missing types (parent deed, EC, khata, mutation, court order, "
        "bank NOC, building approval, survey sketch) when a category is DETECTED or NOT_VERIFIED "
        "and the type is not already uploaded."
    )
    pdf.subsection("I. Local integrity method")
    pdf.body(
        "Finalize builds report_content (property, documents, findings, evidence, mismatches, "
        "unverified, recommendations, disclaimer). report_hash = SHA-256 of JSON with sorted "
        "keys and compact separators [8], [11]. The first ledger row uses previous_hash = "
        "GENESIS. record_hash = SHA-256 of {report_id, report_hash, previous_hash, timestamp}. "
        "A later version links to the prior record_hash, selected by report version. Verify "
        "recomputes both hashes and the predecessor link. The on-disk CHAIN.json file states "
        "in plain English that it is not Bitcoin or Ethereum. A second finalize never edits "
        "the old row; it increments version."
    )
    pdf.numbered(
        [
            "Rebuild canonical JSON from stored report_content with sorted keys.",
            "Compute h1 = SHA-256(canonical). If h1 != report_hash, return TAMPERED.",
            "Rebuild ledger material from report_id, report_hash, previous_hash, hashed_at.",
            "Compute h2 = SHA-256(material). If h2 != record_hash, return TAMPERED.",
            "If version is first, previous_hash must be GENESIS; else it must equal the prior version's record_hash.",
            "If all checks hold, return VALID. Never treat the stored hex string as proof by itself.",
        ]
    )
    pdf.subsection("J. Evaluation method")
    pdf.body(
        "Phase II and case-level behaviour are locked by pytest with mocked Sarvam [10]. "
        "Live UI tests require SARVAM_API_KEY and are not mixed into pytest. Legal language "
        "on screen is constrained: potential issue detected; based on documents provided; "
        "could not be verified. Forbidden: completely safe; legally clear."
    )
    pdf.subsection("K. Worked score and coverage example")
    pdf.body(
        "Suppose a case has one analyzed Kannada sale deed. Litigation is DETECTED HIGH "
        "(stay and pending O.S.). Ownership is DETECTED MEDIUM (seller or buyer name missing). "
        "Mortgage, approval, and property record are NOT_VERIFIED, and no EC, approval, or "
        "sketch has been uploaded. Then |HIGH|=1, |MEDIUM|=1, |LOW|=0, so score = min(100, "
        "70+15) = 85 and overall HIGH. Coverage weights are 1.0, 1.0, 0.0, 0.0, 0.0, so "
        "coverage% = 40. After an EC with explicit nil encumbrance is analyzed and the case "
        "is recalculated, mortgage may become NO_ISSUE_FOUND. Score stays 85 if litigation "
        "and ownership are unchanged, but coverage becomes 60%. That is the point of two "
        "meters: adding a clearing paper improves completeness without pretending the stay "
        "order disappeared."
    )
    pdf.subsection("L. Recalculate versus Analyze")
    pdf.body(
        "Analyze is allowed to be slow and expensive. Recalculate must be local. The method "
        "therefore stores original_text, translated_text, detected_language, document_type, "
        "and extracted_data on the document row. Case merge reads those columns. If the "
        "first digitise was poor, the buyer must click Analyze again; Recalculate will not "
        "silently invent better OCR. This rule is part of methodology, not an implementation "
        "accident."
    )

    pdf.section("V. System Design")
    pdf.subsection("A. Architecture")
    pdf.body(
        "Phase I layers remain. New routers expose analyze, analysis GET, recommendations, "
        "evidence, recalculate, due-diligence, comparisons, finalize, reports, verify, and "
        "PDF. Analyze timeout at the client is 180 seconds. Sarvam poll is 3 seconds with "
        "a 120 second cap."
    )
    pdf.diagram(
        [
            "  SPA --JWT--> FastAPI routers (analysis, reports)",
            "                 |            |              |",
            "                 v            v              v",
            "           analysis_svc  case_analysis   report + ledger",
            "                 |            |              |",
            "                 v            v              v",
            "           Sarvam I/O    PostgreSQL     SHA-256 + CHAIN.json",
            "           (Analyze only)  stored OCR    (local files + tables)",
        ],
        "Fig. 2. Phase II architecture. Recalculate does not leave the database.",
    )
    pdf.subsection("B. Data model extensions")
    pdf.table(
        ["Entity", "New or used fields", "Role"],
        [
            ["Document", "original_text, translated_text, extracted_data, language, type", "Stored reading"],
            ["Analysis", "status, pipeline_steps, extracted JSON", "One-file run"],
            ["RiskFinding", "category, status, level, summary", "Three-state row"],
            ["EvidenceItem", "source_text, page, field", "Quote"],
            ["Recommendation", "category, document_type, reason", "Missing paper"],
            ["DocumentComparison", "field, values, MATCH/MISMATCH", "Pairwise"],
            ["FinalReport", "version, content, hash, score, coverage", "Immutable version"],
            ["LedgerRecord", "previous_hash, record_hash, hashed_at", "Local chain"],
        ],
        [40, 88, 48],
        "Table I. Phase II entities. UUID keys and ownership checks from Phase I still apply.",
    )
    pdf.subsection("C. Disclaimer design")
    pdf.body(
        "Every stored report includes: This report is an AI-assisted document review and is "
        "based only on the documents provided. It does not replace advice from a qualified "
        "lawyer, surveyor, government authority, or other professional."
    )

    pdf.section("VI. Implementation")
    pdf.subsection("A. Modules")
    pdf.body(
        "sarvam_service.py digitises, polls, reads page blocks, unpacks ZIP downloads, "
        "translates, and extracts. analysis_service.py is the one-file pipeline. "
        "extraction_service.py implements merge and veto. document_classifier.py scores "
        "types and Kannada. risk_engine.py and recommendation_engine.py implement Algorithm 3. "
        "comparison_service.py implements Algorithm 4. scoring_service.py implements the "
        "formulae. hashing.py and ledger_service.py implement integrity. report_pdf.py "
        "writes the buyer PDF. NUL bytes are stripped before PostgreSQL TEXT."
    )
    pdf.subsection("B. API additions")
    pdf.table(
        ["Method", "Path", "Note"],
        [
            ["POST", ".../documents/{doc}/analyze", "May call Sarvam"],
            ["GET", ".../documents/{doc}/analysis", "Latest one-file analysis"],
            ["POST", ".../{id}/recalculate", "No Sarvam"],
            ["GET", ".../{id}/due-diligence", "Same payload as recalculate"],
            ["GET", ".../{id}/comparisons", "Stored pairs"],
            ["POST", ".../{id}/finalize", "New version + ledger"],
            ["GET", ".../reports/{rid}/verify", "VALID or TAMPERED"],
            ["GET", ".../reports/{rid}/pdf", "Download"],
        ],
        [22, 88, 66],
        "Table II. Phase II routes. All except health still require JWT and owner checks.",
    )
    pdf.subsection("C. Frontend")
    pdf.body(
        "Document vault offers Analyze and Recalculate. Analysis shows pipeline steps "
        "(uploaded, reading, extracting, checking, complete), extracted groups, and evidence. "
        "Due diligence shows overall level, score /100, coverage %, five cards, and the "
        "comparison table. Finalize warns that some checks may remain unverified and that "
        "missing documents do not block the report. The in-app chat page is a demo helper "
        "and is not the Sarvam path."
    )
    pdf.subsection("D. Implementation limits that are features")
    pdf.bullets(
        [
            "Frontend never submits a trusted score; the server recomputes.",
            "Non-residential analysis remains gated as in Phase I.",
            "Subscription and social login remain non-functional screens.",
        ]
    )

    pdf.section("VII. Results and Discussion")
    pdf.subsection("A. Automated results")
    pdf.body(
        "Phase 2 tests (7) prove analyze requires auth, mocked OCR completes, 403/404 hold, "
        "explicit litigation becomes DETECTED, empty evidence does not become NO_ISSUE_FOUND, "
        "and recommendations appear. Case-level tests (19 in test_phase3.py, treated here as "
        "the Phase II diligence suite) prove name fallbacks, survey prefix MATCH, survey and "
        "area MISMATCH, recalculate merge, EC clearing mortgage, coverage, deterministic score, "
        "GENESIS linkage, second-version previous_hash, VALID on untouched JSON, TAMPERED on "
        "modified JSON, and 403 on a foreign report. Together with Phase I, the repository "
        "holds 39 test functions. Pytest does not call live Sarvam."
    )
    pdf.table(
        ["Observation", "Rule confirmed"],
        [
            ["No EC uploaded", "Mortgage stays NOT_VERIFIED"],
            ["EC with nil encumbrance + recalculate", "Mortgage may become NO_ISSUE_FOUND"],
            ["Survey 45/3 vs 45/4", "MISMATCH HIGH"],
            ["Sy. No. 45/3 vs Survey No. 45/3", "MATCH after normalize"],
            ["Stay/O.S. language in OCR", "Litigation DETECTED even if extract omitted it"],
            ["Score only DETECTED HIGH", "70 points, overall HIGH"],
            ["All NOT_VERIFIED", "Score 0, coverage may still be low"],
            ["Edited report JSON", "verify returns TAMPERED"],
            ["Unedited finalize", "verify returns VALID"],
        ],
        [88, 88],
        "Table III. Qualitative results from the mocked suite and the documented Kannada deed walkthrough.",
    )
    pdf.subsection("B. Live walkthrough")
    pdf.body(
        "With SARVAM_API_KEY set, a Kannada litigation sale deed is the main demonstration. "
        "Litigation is DETECTED at HIGH when stay, pending O.S., or transfer restriction "
        "appears. Mortgage and approval remain NOT_VERIFIED until supporting papers are "
        "analyzed. An early live failure (OCR download was a ZIP) was fixed by unpacking "
        "ZIP payloads in sarvam_service.py; that is an engineering result, not a change of method."
    )
    pdf.subsection("C. Why this is not a trivial wrapper")
    pdf.body(
        "A wrapper would show vendor JSON and a green badge. Phase II adds a veto, a third "
        "status, a compare function with units, two different meters, and a recomputed chain. "
        "Those pieces are short in lines of code and long in specification, which is why "
        "they are written as algorithms and formulae rather than as a tool list [5], [7]."
    )
    pdf.subsection("D. Consistency of terms")
    pdf.body(
        "DETECTED, NO_ISSUE_FOUND, and NOT_VERIFIED are the only category statuses. MATCH, "
        "MISMATCH, and NOT_AVAILABLE are the only comparison results. Coverage uses Verified, "
        "Partially Verified, and Not Verified as labels on the five-category checklist; they "
        "are not a fourth risk status. Ledger means the local GENESIS hash chain in "
        "PostgreSQL and CHAIN.json. Blockchain, wallet, mining, and smart contract do not "
        "appear as implemented features. Phase I words (vault, case, buyer) keep the same "
        "meaning."
    )
    pdf.subsection("E. Threats to validity")
    pdf.body(
        "Internal validity of the rule tests is high because Sarvam is mocked and the "
        "database is in-memory. External validity of live OCR is limited to scan quality "
        "and one vendor. Construct validity of risk is limited by design: the score is not "
        "a probability of losing title. Conclusion validity is protected by the disclaimer "
        "and by forbidding legally clear. Those threats are stated so the paper cannot be "
        "read as a larger study than it is."
    )
    pdf.subsection("F. Limitations")
    pdf.bullets(
        [
            "OCR quality and vendor uptime bound live accuracy.",
            "Kannada party names still fail on some scans; incomplete ownership stays DETECTED.",
            "Boundary lines can concatenate during OCR.",
            "Hindi, Tamil, and other scripts are not first-class.",
            "The ledger is local; it is not a public timestamp authority [8], [9].",
            "No government fetch; no production hardening.",
        ]
    )

    pdf.section("VIII. Conclusion")
    pdf.body(
        "Phase II reads residential papers with Indic document AI and then refuses to let "
        "that AI decide risk. Five categories receive DETECTED, NO_ISSUE_FOUND, or "
        "NOT_VERIFIED. Silence stays unverified. Files are compared without an LLM. Score "
        "and coverage are not the same number. A finalized report can be shown VALID or "
        "TAMPERED by recomputing SHA-256 on a local GENESIS chain. The work does not claim "
        "a clean title and does not claim a public blockchain."
    )
    pdf.body(
        "Future enhancement includes better Kannada name recognition, optional additional "
        "languages, lawful government APIs if they exist, RFC 3161 timestamps, and a human "
        "override with an audit note. None of those items are required to understand or "
        "reproduce the Phase II method described here."
    )

    pdf.section("References")
    refs = [
        "[1]  The Transfer of Property Act, 1882 (India).",
        "[2]  The Registration Act, 1908 (India).",
        "[3]  Sarvam AI, Document AI and translation documentation. [Online]. Available: https://www.sarvam.ai/",
        "[4]  Unicode Consortium, Kannada block U+0C80 to U+0CFF.",
        "[5]  I. Sommerville, Software Engineering, Pearson.",
        "[6]  U. Pal and B. B. Chaudhuri, Indian script character recognition: a survey, Pattern Recognition, 2004.",
        "[7]  IEEE Std 830, IEEE Recommended Practice for Software Requirements Specifications.",
        "[8]  NIST, FIPS PUB 180-4, Secure Hash Standard (SHS), SHA-256.",
        "[9]  C. Adams, P. Cain, D. Pinkas, and R. Zuccherato, Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP), RFC 3161, 2001. Cited as future work only.",
        "[10] pytest documentation. [Online]. Available: https://docs.pytest.org/",
        "[11] T. Bray, The JavaScript Object Notation (JSON) Data Interchange Format, RFC 8259, 2017.",
        "[12] S. Grinberg, FastAPI documentation. [Online]. Available: https://fastapi.tiangolo.com/",
        "[13] PostgreSQL Global Development Group, PostgreSQL 16 documentation.",
        "[14] M. Jones, J. Bradley, and N. Sakimura, JSON Web Token (JWT), RFC 7519, 2015.",
        "[15] R. S. Pressman, Software Engineering: A Practitioner's Approach, McGraw-Hill.",
        "[16] Government of Karnataka, public descriptions of Bhoomi and Kaveri. Not accessed by this software.",
        "[17] OWASP Foundation, File Upload Cheat Sheet (Phase I storage still in force).",
        "[18] Meta Open Source, React documentation. [Online]. Available: https://react.dev/",
    ]
    pdf.set_font("Times", "", 9)
    for ref in refs:
        if pdf.get_y() + 8 > pdf.page_break_trigger:
            pdf.add_page()
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 4.7, ascii(ref))
        pdf.ln(0.4)


def main():
    pdf = AcademicPaper("BhoomiScan Phase II  |  Hybrid reading and three-state risk")
    fill(pdf)
    export_pdf(pdf, "BhoomiScan_Phase2_Paper.pdf")


if __name__ == "__main__":
    main()
