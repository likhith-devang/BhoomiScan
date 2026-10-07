# BhoomiScan Phase 1 — Test Case Report

**Product:** BhoomiScan — Your AIvocate.  
**Phase:** 1 (foundation: auth, property cases, document upload)  
**Date:** 15 September 2026  
**Result:** **13 / 13 automated tests passed.** 7 / 7 manual UI cases passed.  
**Duration:** 7.14 seconds  
**Suite:** `backend/tests/test_phase1.py`

---

## 1. Summary

| Metric | Value |
| --- | --- |
| Automated passed | 13 |
| Automated failed | 0 |
| Automated skipped | 0 |
| Manual UI passed | 7 |
| Pytest | 9.1.1 |
| Python | 3.14.7 |
| Platform | Windows 10 (win32) |
| Test DB | SQLite in-memory (isolated per case) |
| Runtime DB | PostgreSQL 16 (Docker) |

**Verdict:** Phase 1 acceptance tests passed. AI analysis, OCR, Sarvam, risk detection and blockchain are out of scope and were not tested.

---

## 2. Environment

| Item | Value |
| --- | --- |
| Harness | pytest 9.1.1 + FastAPI TestClient |
| Backend | FastAPI / SQLAlchemy |
| Frontend | React + Vite at http://localhost:5173 |
| Auth | JWT (HS256), bcrypt password hashes |
| Warning | Starlette TestClient httpx deprecation (non-blocking) |

### Re-run automated tests

```bash
cd backend
.\.venv\Scripts\activate
pytest -v
```

---

## 3. Automated test cases

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
**Actual:** 400, Get Subscription to use this.  
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

## 4. Manual UI test cases

Exercised against the running app at http://localhost:5173.

| ID | Case | Expected | Actual | Status |
| --- | --- | --- | --- | --- |
| TC-14 | Landing branding | BhoomiScan, Your AIvocate, Get Started, Login | Rendered | Pass |
| TC-15 | Signup → login | Dashboard welcome for new user | Welcome, phase1user | Pass |
| TC-16 | Demo social login | Google/X/phone show Demo only | Demo only, no OAuth | Pass |
| TC-17 | Route protection | /dashboard and /property-domain redirect to /login when logged out | Redirected | Pass |
| TC-18 | Residential flow | Domain → type → case upload page | Upload page opened | Pass |
| TC-19 | Premium domains | Agricultural / Commercial / Industrial show Get Subscription | Get Subscription | Pass |
| TC-20 | Upload papers | PDF stored on residential case | SaleDeed.pdf stored | Pass |

---

## 5. Requirement traceability

| Phase 1 requirement | Covered by |
| --- | --- |
| Signup, unique username, hashed password | TC-01, TC-02, TC-03 |
| Login / invalid login | TC-04, TC-05 |
| JWT `/auth/me` | TC-06, TC-07 |
| Residential property case | TC-08, TC-09, TC-18 |
| Unauthorized / missing case | TC-11, TC-12, TC-17 |
| Document upload and validation | TC-10, TC-13, TC-20 |
| Landing → signup → login → dashboard | TC-14, TC-15 |
| Demo Google / X / phone | TC-16 |
| Non-residential → Get Subscription | TC-09, TC-19 |
| Document upload and validation | TC-10, TC-13, TC-20 |
| Landing → signup → login → home | TC-14, TC-15 |
| Demo Google / X / phone | TC-16 |

---

## 6. Out of scope (not tested)

- Sarvam AI  
- OCR / translation / extraction  
- Risk detection  
- Blockchain / tamper-evident records  
- Google, X, and phone authentication (UI only)
