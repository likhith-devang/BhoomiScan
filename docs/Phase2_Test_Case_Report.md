# BhoomiScan Phase 2 — Test Case Report

**Product:** BhoomiScan — Your AIvocate.  
**Phase:** 2 (AI document analysis: OCR, translation, classification, risk engine)  
**Date:** 15 September 2026  
**Result:** **7 / 7 automated Phase 2 tests passed.** Phase 1 still **13 / 13 passed** in the same run.  
**Last combined pytest:** 20 passed in ~21.5 seconds  
**Suite:** `backend/tests/test_phase2.py`

---

## 1. Summary

| Metric | Value |
| --- | --- |
| Phase 2 automated passed | 7 |
| Phase 2 automated failed | 0 |
| Combined Phase 1 + 2 | 20 / 20 |
| Pytest | 9.1.1 |
| Python | 3.14.7 |
| Platform | Windows 10 (win32) |
| Test DB | SQLite in-memory |
| Sarvam in pytest | Mocked (no live API) |

**Verdict:** Phase 2 automated tests passed. Risk decisions are made by Python rules. Missing documents stay NOT_VERIFIED, not “no issue found”.

---

## 2. Environment

| Item | Value |
| --- | --- |
| Harness | pytest + FastAPI TestClient |
| Backend | FastAPI / SQLAlchemy |
| Frontend | React + Vite at http://localhost:5173 |
| Auth | Existing Phase 1 JWT |
| AI | Sarvam Document AI (live UI only; mocked in tests) |
| Endpoints | POST/GET analyze, recommendations, evidence |

### Re-run

```bash
cd backend
.\.venv\Scripts\activate
pytest tests/test_phase2.py -v
pytest tests/test_phase1.py tests/test_phase2.py -v
```

---

## 3. Automated test cases

### TC-21 — Analyze requires authentication
**Function:** `test_analyze_requires_authentication`  
**Objective:** Analysis cannot run anonymously.  
**Steps:** `POST /property-cases/{id}/documents/{id}/analyze` with no JWT.  
**Expected:** 401.  
**Actual:** 401.  
**Status:** Pass

### TC-22 — Analyze uploaded PDF (mocked Sale Deed)
**Function:** `test_analyze_uploaded_pdf`  
**Objective:** Pipeline classifies a Sale Deed, detects litigation, and does not treat missing papers as clear.  
**Steps:** Upload PDF. Mock Kannada OCR + English translation. `POST .../analyze`. GET analysis.  
**Expected:** 200. SALE_DEED. COMPLETE. Litigation DETECTED / HIGH. Mortgage NOT_VERIFIED. Approval NOT_VERIFIED. Recommendations present.  
**Actual:** As expected.  
**Status:** Pass

### TC-23 — Cannot analyze another user's document
**Function:** `test_user_cannot_analyze_another_users_document`  
**Objective:** Cross-user analysis is forbidden.  
**Steps:** Owner uploads. Second user POSTs analyze.  
**Expected:** 403.  
**Actual:** 403.  
**Status:** Pass

### TC-24 — Missing document returns 404
**Function:** `test_missing_document_returns_404`  
**Objective:** Unknown document UUID cannot be analyzed.  
**Steps:** Create a case. Analyze a random document id.  
**Expected:** 404.  
**Actual:** 404.  
**Status:** Pass

### TC-25 — Litigation detected from explicit evidence
**Function:** `test_litigation_detected_from_explicit_evidence`  
**Objective:** Source text wins even if AI JSON leaves stay_order null.  
**Steps:** Mock extract with stay_order null. English text contains O.S. No. 234/2019, pending, stay order, transfer restriction. GET evidence.  
**Expected:** DETECTED, case number 234/2019, stay true, evidence list non-empty.  
**Actual:** As expected.  
**Status:** Pass

### TC-26 — Empty evidence does not produce NO_ISSUE_FOUND
**Function:** `test_empty_evidence_does_not_produce_no_issue_found`  
**Objective:** Absence of court language is not proof of no litigation.  
**Steps:** Analyze a clean Sale Deed with no court language.  
**Expected:** Litigation, Mortgage, Approval = NOT_VERIFIED. Litigation is not NO_ISSUE_FOUND.  
**Actual:** As expected.  
**Status:** Pass

### TC-27 — Recommendation engine
**Function:** `test_recommendation_engine_returns_missing_documents`  
**Objective:** Unresolved risks recommend next papers.  
**Steps:** Analyze mocked litigation Sale Deed. `GET /property-cases/{id}/recommendations`.  
**Expected:** Includes ENCUMBRANCE_CERTIFICATE, COURT_ORDER, BUILDING_PLAN_APPROVAL.  
**Actual:** As expected.  
**Status:** Pass

---

## 4. Manual / live cases

| ID | Case | Expected | Status |
| --- | --- | --- | --- |
| TC-20 | Analyze Document UI | Real analyze, not a Phase 2 toast | Pass |
| TC-28 | Risk cards | Five categories after success | Confirm on successful run |
| TC-29 | Live Kannada PDF | SaleDeed_01_Litigation_Kannada.pdf via Sarvam | Retest after OCR ZIP fix |

**Note:** First live Sarvam run failed because OCR download is a ZIP. Backend now reads structured get_results text. Click Run analysis again.

---

## 5. Requirement traceability

| Requirement | Cases |
| --- | --- |
| Analyze requires login | TC-21 |
| User cannot analyze another user's document | TC-23 |
| Missing document 404 | TC-24 |
| Classify Sale Deed | TC-22 |
| Litigation DETECTED from source evidence | TC-22, TC-25 |
| Mortgage / approval NOT_VERIFIED without papers | TC-22, TC-26 |
| Absence is not NO_ISSUE_FOUND | TC-26 |
| Evidence attached | TC-25 |
| Recommendations | TC-27 |
| Phase 1 still passes | test_phase1.py TC-01–TC-13 |

---

## 6. Out of scope

- Blockchain / SHA-256 final report  
- Downloadable multi-document due-diligence report  
- Cross-document comparison  
- Real payments  
- Real Google / X / phone login  
- Live Sarvam inside pytest
