# Mental Health Recovery Prediction Platform

## 1. Executive Overview
The project is an AI-enabled clinical decision support application that predicts mental health recovery time (in weeks), explains why via Hybrid XAI (rule-based + RAG + planned SHAP/LIME), and provides an in-domain restricted conversational assistant. It combines a FastAPI backend, a React/Vite/Tailwind frontend, a stacking ensemble regression model, and a Retrieval-Augmented clinical + application knowledge system.

Key feature pillars:
1. Prediction Engine (Stacking Ensemble with 80 engineered features derived from 22 input fields)
2. Explanation System (RAG-based clinical reasoning + factor extraction + future SHAP/LIME hooks)
3. Domain-Restricted RAG Chatbot (Gemini-powered with semantic + rule filters)
4. Batch Processing & Reporting (CSV bulk inference + PDF report generation)
5. History & Persistence (JSON storage with risk flagging & comparison to doctor-prescribed timeline)

---
## 2. High-Level Data & Control Flow
```
Frontend (React) → /api/predict (FastAPI) → MLInference
                                 ↓
                         Prediction dict
                                 ↓
                    Persist to predictions.json
                                 ↓
User triggers /api/explain → RAGEngine.generate_explanation
                                 ↓
User optionally chats → /api/chat → ChatbotEngine.get_response (Domain Validation → Intent → Gemini/KB)
                                 ↓
User downloads /api/report/{id} → PDF via wkhtmltopdf
                                 ↓
History endpoints for retrieval, CSV upload for batch predictions
```

---
## 3. Directory & Component Mapping
- `backend/app/main.py`: FastAPI app bootstrap, middleware, router inclusion, startup model preload.
- `backend/app/config.py`: Central settings (paths, model metrics, API keys).
- `backend/app/models/schemas.py`: Pydantic schemas for patient input, prediction, explanation, health check.
- `backend/app/api/`: REST endpoints (`predict`, `explain`, `chatbot`, `upload`, `report`, `history`).
- `backend/app/services/`:
  - `ml_inference.py`: Core inference + feature engineering expansion (22 → 80).
  - `rag_engine.py`: Clinical explanation builder (rule/RAG hybrid, SHAP/LIME placeholder).
  - `chatbot_engine.py`: Domain-restricted RAG + Gemini chatbot.
  - `predictions_storage.py`: Lightweight JSON persistence layer.
  - `file_parser.py`: CSV parsing helper.
  - `compatibility.py`: Scikit-learn stacking compatibility wrappers.
- `backend/data/`: Knowledge bases (`clinical_knowledge.txt`, `chatbot_knowledge.txt`), dynamic predictions file.
- `backend/ml_models/FINAL_best_model_stacking-ensemble-8.joblib`: Serialized package containing `model`, `scaler`, `feature_names`, encoders, metadata.
- Frontend directories (`mental-health-frontend/`, `inner-bloom-main/`): React components consuming API.

---
## 4. Configuration & Environment
`Settings` class initializes data and upload directories, exposes model path, metrics (R², RMSE, MAE), and API keys for Gemini / OpenAI / Anthropic (only Gemini actively used). Model performance constants are embedded for immediate reuse in responses (confidence handling, intervals).

---
## 5. Patient Input → Feature Engineering → Prediction
### 5.1 Canonical Input (22 Fields)
Incoming JSON conforms to `PatientInput` with structured demographic, clinical, treatment, lifestyle, and optional comparison fields (`doctor_prescribed_weeks`, `family_history_relationship`).

### 5.2 Mapping & Normalization (`MLInference._build_raw_row`)
- Applies defaults for missing numeric (`RAW_DEFAULTS_NUM`) and categorical (`RAW_DEFAULTS_CAT`) fields.
- Converts booleans & yes/no medication flags to categorical encodings handled by saved label encoders.
- Ensures robust casting with `_safe_float` / `_safe_int` to prevent pipeline failure.

### 5.3 Expansion to 80 Engineered Features (`_expand_to_80_features`)
Driven by `feature_names` loaded from the model package. Dynamically computes feature values on demand:
- Arithmetic combinations: `A_div_B`, `A_x_B`.
- Polynomial terms: `_sq`, `_cb`.
- Root transforms: `_sqrt`.
- Aggregate statistics: `sum_`, `mean_`, `std_`, `max_`, `min_`, `range_`.
- Falls back to `0.0` for any unexpected engineered symbol to preserve column alignment.

### 5.4 Scaling & Inference
- Applies model-associated scaler if present to ordered feature matrix.
- Performs prediction through stacked ensemble (meta-regressor over base learners). Clamps prediction to plausible range `[5, 20]` weeks (business logic constraint).

### 5.5 Output Structure
Prediction response includes:
- Point estimate (`prediction_weeks`).
- Model confidence (`confidence` = stored R²).
- Error & range (`error_margin` = MAE, plus `prediction_range`).
- Interpretation bucket (fast/standard/extended recovery via thresholds).
- Computed 95% interval using RMSE (`_compute_confidence_interval`).
- Base model breakdown (if stacking exposes `.estimators_`).
- Risk flags (severity/social support/comorbidities/older age/no medication) assembled by `_risk_flags_for_patient`.
- Doctor comparison (difference and recommendation heuristic) if `doctor_prescribed_weeks` provided.

---
## 6. Persistence Layer (`predictions_storage.py`)
- JSON file at `data/predictions.json` keyed by UUID `prediction_id`.
- Each record contains original patient data & derived prediction metadata.
- Retrieval: `load_all()` sorts by `timestamp` (with fallback blank). Note: `clear_all()` references `_save_to_file()` which is absent—this is a minor implementation inconsistency (future fix: unify internal method names to `_write`).

---
## 7. CSV Batch Upload (`upload.py`)
- Accepts arbitrary column naming; attempts canonical 22-field extraction via `pick()` fallback logic.
- Normalizes types (notably `income_level`, `medication`, booleans).
- Iteratively calls `MLInference.predict()` per row; returns per-row minimal prediction summary (weeks, confidence, interpretation). This leverages the same feature engineering path guaranteeing consistency across single and batch modes.

---
## 8. Report Generation (`report.py`)
- Uses `pdfkit` with explicit Windows path to `wkhtmltopdf`.
- Builds structured HTML (patient data table + summary + interpretation) → PDF streamed as `FileResponse`.
- Error handling wraps generation; missing record triggers 404.

---
## 9. Explanation System (RAG + Rule-Based Clinical Reasoning)
### 9.1 Current Implementation
`RAGEngine.generate_explanation()` composes an explanation object:
- Parses critical factors (age, severity, support, diagnosis, therapy, medication, family history, comorbidity).
- Builds multi-section narrative (profile analysis, factors list, recommendations, confidence statement).
- Extracts key factors & clinical reasoning using structured helper functions (`_extract_key_factors`, `_extract_reasoning`).
- Returns citations (static curated list) to support academic grounding.

### 9.2 Knowledge Base Utilization
- Loads content from `clinical_knowledge.txt` (currently empty; fallback sample content seeded if absent).
- Suggestion: populate this file with structured evidence (guidelines, recovery timelines, scoring criteria) to strengthen retrieval.

### 9.3 SHAP & LIME Hooks
- `initialize_explainers(model, data)` method prepared to instantiate `shap.Explainer` and `lime_tabular.LimeTabularExplainer`.
- Not yet invoked by API—representing planned deep feature-attribution integration.
- Future path: precompute background dataset & persist shap value cache for faster per-request introspection.

### 9.4 XAI Strategy Layered
1. Deterministic clinical heuristic summarization (rules mapping severity/age/support → natural language).
2. RAG narrative referencing knowledge base (currently static fallback).
3. Planned model-level attribution (SHAP global + LIME local per patient).
4. Interval communication (RMSE-based 95% range informs uncertainty transparency).

---
## 10. Chatbot Architecture (Domain-Restricted RAG + Gemini)
### 10.1 Flow
```
User message → Intent Classification (greeting/farewell/crisis/etc.)
    → (if greeting/farewell) direct template response
    → Domain Validation (_is_in_domain) → confidence score
         ↳ reject → curated out-of-domain guidance
         ↳ accept → crisis check → Gemini or KB fallback response
```

### 10.2 Domain Validation Mechanics
- Reject list: fast exclusion (weather, sports, politics...).
- Allowed domain keyword set (mental health, recovery, app usage, treatment, coping...).
- Overlap scoring: keyword intersections between query tokens and KB tokens (50% weight).
- Pattern matching (question forms, mental health phrasing) adds context weight.
- Composite confidence threshold (≥0.6 required). Response envelope returns `domain_confidence`.

### 10.3 Response Generation
- Primary: Gemini model (`gemini-2.0-flash`) with explicit domain restriction prompt.
- Fallback: Knowledge base section extraction + structured markdown assembly.
- Crisis detection triggers priority safety protocol with hotline resources.

### 10.4 Conversation Management
- Keeps last 20 exchanges (`conversation_history`). History retrieval and clearing exposed via API endpoints.
- Suggested questions list fosters guided exploration of capabilities.

---
## 11. Knowledge Bases
- `chatbot_knowledge.txt`: Rich, multi-section domain document (conditions, treatments, usage, ethics, troubleshooting). Powers keyword overlap for domain validation and fallback generation.
- `clinical_knowledge.txt`: Currently empty (immediate enhancement opportunity). Fallback seeds minimal recovery timeline text if absent.

Enhancement: Introduce embedding store (e.g., sentence-transformers + vector index) to move from lexical overlap to semantic retrieval for RAGEngine & chatbot.

---
## 12. Frontend Integration (High-Level)
Although not fully inspected here, typical flow:
- Form component captures `PatientInput` fields → POST `/api/predict`.
- Displays prediction card with intervals, risk flags, base model breakdown.
- Button triggers POST `/api/explain` with patient + prediction metadata → shows narrative & factors.
- Chat interface streams queries to `/api/chat` with suggestions & domain feedback.
- History panel fetches `/api/history` for recent predictions, linking to report downloads.
- CSV upload widget posts file to `/api/upload` and renders batch results.

---
## 13. Explainability (XAI) Deep Dive
| Layer | Purpose | Status |
|-------|---------|--------|
| Rule/Heuristic | Immediate human-readable factors | Active |
| RAG Narrative | Contextual clinical reasoning | Active (lexical) |
| SHAP Values | Global/local feature contribution | Scaffolded (not wired) |
| LIME | Local perturbation-based explanation | Scaffolded (not wired) |
| Confidence Interval | Uncertainty quantification | Active |
| Risk Flags | Clinical risk heuristics | Active |

Planned integration path:
1. Load representative background dataset (e.g., 100 stratified patient rows) on startup.
2. Call `RAGEngine.initialize_explainers(model, background_df)` after `MLInference` loads.
3. Add endpoint `/api/explain/attribution` returning top SHAP contributors + localized LIME weights.
4. Merge attributions into existing narrative (e.g., “Most influential features: Severity_Score (↑), Social_Support_Level (↓), Age (↑)”).

---
## 14. End-to-End Prediction Lifecycle
1. User submits form → `POST /api/predict`.
2. API validates via Pydantic `PatientInput` (range constraints protect model assumptions).
3. Model loaded (singleton pattern ensures single memory instance) if not already.
4. Input mapped → raw → expanded → scaled.
5. Stacking ensemble produces weeks estimate; clamps outliers.
6. Confidence & intervals derived from persisted metrics (RMSE, MAE, R²) rather than recalculated.
7. Risk flags & doctor comparison appended.
8. Result persisted and returned.
9. User optionally requests explanation → RAGEngine builds narrative.
10. User may download PDF → HTML → wkhtmltopdf.
11. Records browsed via history; possibly batch processed via CSV.

---
## 15. Security, Reliability & Ethical Considerations
- Domain restriction prevents unsafe or irrelevant chatbot responses (reduces misuse scope).
- Absence of direct PHI storage (fields are clinical but can be anonymized; recommend enforced hashing for identifiers if added).
- Confidence/interval disclosure fosters responsible interpretation (discourages deterministic treatment changes).
- Crisis intent branch ensures safety guidance promptly.
- Ethical risk: Synthetic training data—clarify generation pipeline and limitations in paper.

Hardening suggestions:
- Add request rate limiting (FastAPI middleware) for chat endpoints.
- Validate PDF generation path to avoid path traversal (currently fixed filename pattern).
- Implement structured logging with correlation IDs for audit.
- Add schema versioning for `PatientInput` to prevent silent model drift.

---
## 16. Limitations & Future Enhancements
| Area | Current | Limitation | Proposed Improvement |
|------|---------|-----------|----------------------|
| RAG | Lexical overlap | Shallow semantic match | Vector embeddings + ANN index |
| XAI | Narrative heuristics | No numeric attribution surfaced | Wire SHAP/LIME outputs into API |
| Persistence | Flat JSON | No concurrency control | SQLite/Postgres + migration strategy |
| Model | Static ensemble | No online adaptation | Periodic retraining + drift monitoring |
| Chatbot | Single LLM fallback | No multi-model arbitration | Add fallback providers + response quality scoring |
| Clinical KB | Sparse (empty file) | Limited evidence depth | Structured ingestion (PubMed summarization) |

---
## 17. Draft Academic / Project Paper Guidance
Suggested Section Outline:
1. Abstract – Problem statement (mental health recovery prediction), approach (ensemble + explainability + domain-restricted RAG), outcomes.
2. Introduction – Motivation, clinical relevance, gaps in existing tooling.
3. Related Work – Recovery prediction methods, XAI in healthcare, RAG architectures, conversational safety.
4. System Architecture – Diagrams (overall data flow, chatbot domain filter pipeline, model feature engineering chain).
5. Methods – Data synthesis, feature engineering taxonomy, stacking ensemble configuration, confidence interval logic.
6. Explainability – Multi-layer XAI (heuristics, RAG, planned SHAP/LIME), risk flags, interpretability rationale.
7. Chatbot Domain Restriction – Scoring formula, thresholds, rejection policy, safety protocols.
8. Evaluation – Model performance metrics (R², RMSE, MAE), qualitative explanation assessment, domain filtering precision/recall (future experiment: labeled queries dataset).
9. Ethical & Privacy Considerations – Data use, limitations of synthetic data, escalation mechanisms.
10. Limitations & Future Work – As enumerated; embedding-based RAG, attribution integration.
11. Conclusion – Summary and value proposition for clinical decision support.
12. References – DSM-5, APA guidelines, SHAP, LIME foundational papers, ensemble regression literature, RAG survey papers.

---
## 18. Glossary (Selected)
- RAG (Retrieval-Augmented Generation): Combining retrieved contextual documents with generative model prompting.
- SHAP: SHapley Additive exPlanations; game-theoretic feature attribution method.
- LIME: Local Interpretable Model-agnostic Explanations; perturbation-based local surrogate modeling.
- Stacking Ensemble: Meta-learning approach combining multiple base estimators’ outputs.
- RMSE / MAE: Error metrics (Root Mean Squared Error, Mean Absolute Error) used for interval & range estimation.
- Confidence (here): Proxy using stored R² metric—not calibrated probability.
- Risk Flags: Rule-derived clinical risk indicators augmenting model output.

---
## 19. Quick Improvement Checklist (Actionable)
- Populate `clinical_knowledge.txt` with structured clinical evidence.
- Add explainer initialization at startup for SHAP/LIME.
- Implement `/api/explain/attribution` endpoint.
- Replace JSON storage with ACID-compliant DB.
- Integrate semantic embeddings for chatbot & explanation retrieval.
- Add unit tests for feature expansion & risk flag logic.
- Harden domain rejection with confusion matrix evaluation.

---
## 20. Summary
The platform implements a layered architecture balancing predictive accuracy, interpretability, and domain-safe user interaction. Core strengths lie in deterministic feature expansion, structured prediction responses, and robust domain gating for the chatbot. Future efforts should focus on deeper semantic retrieval, operational robustness (database + test coverage), and fully realized model attribution.

This document serves as a comprehensive reference for explaining functionality to stakeholders and drafting academic or technical papers.
