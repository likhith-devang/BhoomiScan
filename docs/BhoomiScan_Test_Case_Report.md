# BhoomiScan — Test Case Report

**Product:** BhoomiScan — Your AIvocate.  
**Phases covered:** Phase 1 (auth, property cases, document upload) and Phase 2 (AI document analysis)  
**Date:** 15 September 2026  
**Automated result:** **20 / 20 passed** (13 Phase 1 + 7 Phase 2)  
**Duration (last run):** ~21.5 seconds  
**Suites:** `backend/tests/test_phase1.py`, `backend/tests/test_phase2.py`

---

## 1. Summary

| Metric | Value |
| --- | --- |
| Automated passed | 20 |
| Automated failed | 0 |
| Automated skipped | 0 |
| Phase 1 tests | 13 |
| Phase 2 tests | 7 |
| Pytest | 9.1.1 |
| Python | 3.14.7 |
| Platform | Windows 10 (win32) |
| Test DB | SQLite in-memory (isolated per case) |
| Runtime DB | PostgreSQL 16 (Docker) |

**Verdict:** Automated acceptance tests passed. Phase 1 still passes after Phase 2 was added. Pytest mocks Sarvam; live OCR uses `SARVAM_API_KEY`.

---

## 2. Environment

| Item | Value |
| --- | --- |
| Harness | pytest + FastAPI TestClient |
| Backend | FastAPI / SQLAlchemy |
| Frontend | React + Vite at http://localhost:5173 |
| Auth | JWT (HS256), bcrypt password hashes |
| Phase 2 AI | Sarvam Document AI (mocked in automated tests) |
| Warning | Starlette TestClient httpx deprecation (non-blocking) |

### Re-run automated tests

```bash
cd backend
.\.venv\Scripts\activate
pytest tests/test_phase1.py tests/test_phase2.py -v
```

---

## 3. Phase 1 automated cases

### TC-01 — Signup success
**Function:** `test_signup_success`  
**Objective:** A new user can register with username and matching passwords.  
**Steps:** `POST /auth/signup` with username `advocate`, password `securePass1`.  
**Expected:** 201. Body has `id` and `username`. Password is not returned.  
**Actual:** 201. `username=advocate`. No `password` / `password_hash`.  
**Status:** Pass

### TC-02 — Duplicate signup
**Function:** `test_duplicate_signup`  
**Objective:** Username must be unique.  
**Steps:** Sign up twice with the same username.  
**Expected:** 409, `Username already exists.`  
**Actual:** 409 with that message.  
**Status:** Pass

### TC-03 — Password mismatch
**Function:** `test_signup_password_mismatch`  
**Objective:** Confirmation must match password.  
**Steps:** Signup with different `confirm_password`.  
**Expected:** 422, detail mentions match.  
**Actual:** 422.  
**Status:** Pass

### TC-04 — Login success
**Function:** `test_login_success`  
**Objective:** Valid credentials return a JWT.  
**Steps:** `POST /auth/login` after signup.  
**Expected:** 200, `token_type=bearer`, non-empty `access_token`.  
**Actual:** 200 with bearer token.  
**Status:** Pass

### TC-05 — Invalid login
**Function:** `test_invalid_login`  
**Objective:** Wrong password is rejected.  
**Steps:** Login with `wrong-password`.  
**Expected:** 401, `Invalid username or password.`  
**Actual:** 401 with that message.  
**Status:** Pass

### TC-06 — Protected endpoint without token
**Function:** `test_protected_endpoint_requires_auth`  
**Objective:** `/auth/me` requires JWT.  
**Steps:** `GET /auth/me` with no header.  
**Expected:** 401.  
**Actual:** 401.  
**Status:** Pass

### TC-07 — Protected endpoint with token
**Function:** `test_protected_endpoint_with_token`  
**Objective:** Valid JWT returns the current user.  
**Steps:** `GET /auth/me` with Bearer token.  
**Expected:** 200, `username=advocate`.  
**Actual:** 200.  
**Status:** Pass

### TC-08 — Property case creation
**Function:** `test_property_case_creation`  
**Objective:** Create an ACTIVE residential case.  
**Steps:** `POST /property-cases` with `RESIDENTIAL` / `APARTMENT_FLAT`.  
**Expected:** 201, `status=ACTIVE`, `document_count=0`.  
**Actual:** 201 as specified.  
**Status:** Pass

### TC-09 — Non-residential domain rejected
**Function:** `test_property_case_rejects_non_residential`  
**Objective:** Agricultural / Commercial / Industrial require a subscription.  
**Steps:** `POST /property-cases` with `COMMERCIAL`.  
**Expected:** 400, message mentions subscription.  
**Actual:** 400, `Get Subscription to use this.`  
**Status:** Pass

### TC-10 — Document upload
**Function:** `test_document_upload`  
**Objective:** Store a PDF on an owned case.  
**Steps:** Create villa case. `POST` `SaleDeed.pdf`. `GET` document list.  
**Expected:** 201, `status=UPLOADED`, `file_type=application/pdf`, list length 1.  
**Actual:** 201 then 200 with one document.  
**Status:** Pass

### TC-11 — Unauthorized case access
**Function:** `test_unauthorized_case_access`  
**Objective:** Users cannot access another user's case.  
**Steps:** Owner creates a case. Second user GET and POST documents.  
**Expected:** 403 on both.  
**Actual:** 403 on GET and POST.  
**Status:** Pass

### TC-12 — Missing property case
**Function:** `test_missing_property_case`  
**Objective:** Unknown UUID returns 404.  
**Steps:** `GET /property-cases/11111111-1111-1111-1111-111111111111`.  
**Expected:** 404.  
**Actual:** 404.  
**Status:** Pass

### TC-13 — Unsupported file
**Function:** `test_unsupported_file`  
**Objective:** Reject files that are not PDF/PNG/JPG.  
**Steps:** Upload `notes.txt` as `text/plain`.  
**Expected:** 400, unsupported.  
**Actual:** 400.  
**Status:** Pass

---

## 4. Phase 2 automated cases

Sarvam Document AI is **mocked**. Tests prove auth, ownership, risk rules, evidence, and recommendations — not the live OCR network call.

### TC-21 — Analyze requires authentication
**Function:** `test_analyze_requires_authentication`  
**Objective:** Analysis cannot run anonymously.  
**Steps:** `POST /property-cases/{id}/documents/{id}/analyze` with no JWT.  
**Expected:** 401.  
**Actual:** 401.  
**Status:** Pass

### TC-22 — Analyze uploaded PDF (mocked Sale Deed)
**Function:** `test_analyze_uploaded_pdf`  
**Objective:** Pipeline classifies a Sale Deed, detects litigation, and does not treat missing papers as “clear”.  
**Steps:** Upload PDF. Mock Kannada OCR + English translation. `POST .../analyze`.  
**Expected:** 200. `document_type=SALE_DEED`. `analysis_status=COMPLETE`. Litigation DETECTED / HIGH. Mortgage NOT_VERIFIED. Approval NOT_VERIFIED. Recommendations present. GET analysis returns the same id.  
**Actual:** As expected.  
**Status:** Pass

### TC-23 — Cannot analyze another user's document
**Function:** `test_user_cannot_analyze_another_users_document`  
**Objective:** Cross-user analysis is forbidden.  
**Steps:** Owner uploads a document. Second user POSTs analyze.  
**Expected:** 403.  
**Actual:** 403.  
**Status:** Pass

### TC-24 — Missing document returns 404
**Function:** `test_missing_document_returns_404`  
**Objective:** Unknown document UUID is not analyzable.  
**Steps:** Create a case. Analyze a random document id.  
**Expected:** 404.  
**Actual:** 404.  
**Status:** Pass

### TC-25 — Litigation detected from explicit evidence
**Function:** `test_litigation_detected_from_explicit_evidence`  
**Objective:** Source text wins even if AI JSON leaves stay_order null.  
**Steps:** Mock extract `{ stay_order: null }` but English text contains O.S. No. 234/2019, pending, stay order, transfer restriction. GET evidence.  
**Expected:** Litigation DETECTED, case number contains 234/2019, stay_order true, evidence list non-empty.  
**Actual:** As expected.  
**Status:** Pass

### TC-26 — Empty evidence does not produce NO_ISSUE_FOUND
**Function:** `test_empty_evidence_does_not_produce_no_issue_found`  
**Objective:** Absence of a court mention is not proof of no litigation.  
**Steps:** Analyze a clean Sale Deed with no court language.  
**Expected:** Litigation, Mortgage, and Approval are NOT_VERIFIED. Litigation is not NO_ISSUE_FOUND.  
**Actual:** As expected.  
**Status:** Pass

### TC-27 — Recommendation engine
**Function:** `test_recommendation_engine_returns_missing_documents`  
**Objective:** Unresolved risks recommend next papers.  
**Steps:** Analyze mocked litigation Sale Deed. `GET /property-cases/{id}/recommendations`.  
**Expected:** 200. Includes ENCUMBRANCE_CERTIFICATE, COURT_ORDER, BUILDING_PLAN_APPROVAL.  
**Actual:** As expected.  
**Status:** Pass

---

## 5. Manual UI cases

Exercised against http://localhost:5173.

| ID | Case | Expected | Status |
| --- | --- | --- | --- |
| TC-14 | Landing | BhoomiScan, Your AIvocate, Login / Get Started | Pass |
| TC-15 | Login → Home | Welcome back + real username; Login hidden | Pass |
| TC-16 | Demo social login | Google / X / phone show Demo only | Pass |
| TC-17 | Route protection | Logged-out `/dashboard` and `/ai` redirect to `/login` | Pass |
| TC-18 | Homes flow | Start Analysis → Homes → type → upload | Pass |
| TC-19 | Premium domains | Agricultural / Commercial / Industrial → Get Subscription | Pass |
| TC-20 | Analyze Document | Real analyze action (not a Phase 2 toast) | Pass |
| TC-28 | Risk UI | Five risk cards after a successful analysis | Confirm on next successful run |
| TC-29 | Live Kannada PDF | `SaleDeed_01_Litigation_Kannada.pdf` through Sarvam | Retest after OCR ZIP fix |

**Note on TC-29:** The first live run failed because Sarvam returns OCR as a ZIP of page blocks. The backend now reads structured `get_results` text. Click **Run analysis again** on that document.

---

## 6. Requirement traceability

| Requirement | Covered by |
| --- | --- |
| Signup, unique username, hashed password | TC-01, TC-02, TC-03 |
| Login / invalid login | TC-04, TC-05 |
| JWT `/auth/me` | TC-06, TC-07 |
| Residential property case | TC-08, TC-18 |
| Non-residential → Get Subscription | TC-09, TC-19 |
| Unauthorized / missing case | TC-11, TC-12, TC-17 |
| Document upload and validation | TC-10, TC-13, TC-20 |
| Analyze requires login | TC-21 |
| User cannot analyze another user's document | TC-23 |
| Missing document 404 | TC-24 |
| Litigation DETECTED from source evidence | TC-22, TC-25 |
| Mortgage / approval NOT_VERIFIED without papers | TC-22, TC-26 |
| Absence ≠ NO_ISSUE_FOUND | TC-26 |
| Evidence attached to findings | TC-25 |
| Recommendations for missing documents | TC-27 |
| Phase 1 still passes after Phase 2 | TC-01–TC-13 |

---

## 7. Out of scope (not tested here)

- Blockchain / SHA-256 final report  
- Downloadable multi-document due-diligence report  
- Cross-document field comparison (Phase 3)  
- Real Google, X, and phone authentication  
- Real payments  
- Live Sarvam inside pytest (always mocked)
