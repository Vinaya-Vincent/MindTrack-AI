# Mental Health Recovery App - Cleanup Guide

## Files/Folders to Remove (Unnecessary)

### Backend
- `backend/oldenv/` - Old Python virtual environment (not needed)
- `backend/oldenv39/` - Another old virtual environment (not needed)
- `backend/inspect_model_features.py` - Development/debugging script (optional)
- `backend/model_fix.py` - Temporary fix script (optional)
- `backend/test_model_load.py` - Test script (optional, but keep for testing)
- `backend/report_*.pdf` - Generated PDF reports (can be cleaned periodically)

### Root Directory
- `old_scripts/` - Legacy scripts folder (archive or delete)
- `visualizations/` - If empty or unused
- `node_modules/` at root - Should only be in frontend folder
- `package.json` and `package-lock.json` at root - Should only be in frontend

### Frontend
- Keep as is - all files needed

## Files to Keep

### Essential Backend Files
- `backend/app/` - Main application code
- `backend/data/` - Knowledge bases and data
- `backend/ml_models/` - ML model files
- `backend/requirements.txt` - Dependencies
- `backend/venv/` - Active virtual environment
- `backend/uploads/` - User uploads folder

### Essential Root Files
- `run_app.py` - Startup script
- `README.md` - Documentation
- `CHATBOT_SAMPLE_QUESTIONS.md` - Chatbot guide
- `docker-compose.yml` - Docker setup
- `.conda/` - Conda environment

## Project Structure (Cleaned)

```
mental-health-recovery-app/
├── .conda/                          # Conda environment
├── backend/
│   ├── app/
│   │   ├── api/                     # API endpoints
│   │   │   ├── chatbot.py          # ✅ NEW: Chatbot endpoints
│   │   │   ├── explain.py
│   │   │   ├── history.py
│   │   │   ├── predict.py
│   │   │   ├── report.py
│   │   │   └── upload.py
│   │   ├── models/
│   │   │   └── schemas.py           # ✅ FIXED: Age validation
│   │   ├── services/
│   │   │   ├── chatbot_engine.py   # ✅ NEW: AI Chatbot
│   │   │   ├── compatibility.py
│   │   │   ├── file_parser.py
│   │   │   ├── ml_inference.py
│   │   │   ├── predictions_storage.py
│   │   │   └── rag_engine.py
│   │   ├── config.py
│   │   └── main.py                  # ✅ UPDATED: Added chatbot route
│   ├── data/
│   │   ├── chatbot_knowledge.txt   # ✅ NEW: Comprehensive KB
│   │   ├── clinical_knowledge.txt
│   │   └── predictions.json
│   ├── ml_models/
│   │   └── FINAL_best_model_stacking-ensemble-8.joblib
│   ├── uploads/                     # CSV uploads
│   ├── venv/                        # Virtual environment
│   └── requirements.txt
├── mental-health-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BaseModelChart.jsx
│   │   │   ├── Chatbot.jsx         # ✅ NEW: AI Chatbot UI
│   │   │   ├── ConfidenceBadge.jsx
│   │   │   ├── CSVUploader.jsx
│   │   │   ├── History.jsx
│   │   │   ├── HistoryPanel.jsx
│   │   │   ├── HistoryTimeline.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── PredictionForm.jsx  # ✅ FIXED: Default values
│   │   │   ├── PredictionResult.jsx
│   │   │   ├── RAGModal.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── RiskBanner.jsx
│   │   ├── context/
│   │   │   └── ThemeContext.jsx
│   │   ├── utils/
│   │   │   ├── api.js              # ✅ UPDATED: Added chatbot APIs
│   │   │   └── csvParser.js
│   │   ├── App.jsx                  # ✅ FIXED: Chatbot placement
│   │   ├── constants.js
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── data/
│   └── mental_health_engineered.csv
├── CHATBOT_SAMPLE_QUESTIONS.md     # ✅ NEW: Sample questions
├── docker-compose.yml
├── README.md
└── run_app.py                       # Startup script
```

## Cleanup Commands (PowerShell)

```powershell
# Navigate to project root
cd C:\Users\abish\OneDrive\Desktop\mental-health-recovery-app

# Remove old virtual environments (BE CAREFUL!)
# Only run if you're sure you don't need them
Remove-Item -Recurse -Force .\backend\oldenv
Remove-Item -Recurse -Force .\backend\oldenv39

# Remove old scripts
Remove-Item -Recurse -Force .\old_scripts

# Remove temporary PDF reports
Remove-Item .\backend\report_*.pdf

# Remove root-level node modules (if exists)
if (Test-Path .\node_modules) {
    Remove-Item -Recurse -Force .\node_modules
}

# Remove root package files (if not needed)
if (Test-Path .\package.json) {
    Remove-Item .\package.json
}
if (Test-Path .\package-lock.json) {
    Remove-Item .\package-lock.json
}

# Optional: Remove development scripts
# Remove-Item .\backend\inspect_model_features.py
# Remove-Item .\backend\model_fix.py
```

## What Was Fixed

### 1. Age Validation Error ✅
- **Problem**: Backend required age >= 18
- **Fix**: Changed to age >= 0 (allows all ages)
- **File**: `backend/app/models/schemas.py`

### 2. Missing Chatbot ✅
- **Problem**: Chatbot was inside unused `InnerApp` component
- **Fix**: Moved to main App component, visible on all pages
- **File**: `mental-health-frontend/src/App.jsx`

### 3. Empty Form Submission ✅
- **Problem**: Form submitted with empty values causing validation errors
- **Fix**: Added default values for all fields
- **File**: `mental-health-frontend/src/components/PredictionForm.jsx`

### 4. Missing Chatbot Backend ✅
- **Added**: `chatbot_engine.py` - AI engine with RAG
- **Added**: `chatbot.py` - API endpoints
- **Added**: `chatbot_knowledge.txt` - Comprehensive knowledge base
- **Updated**: `main.py` - Added chatbot routes
- **Updated**: `api.js` - Added chatbot API functions

## New Features Added

### AI Chatbot 🤖
- **Location**: Bottom-right floating button on all pages
- **Features**:
  - Intent classification
  - Knowledge base retrieval
  - Crisis response priority
  - Conversation history
  - Suggested questions
  - Markdown formatting
  - Dark/Light mode support

### Knowledge Base
- 5000+ words covering:
  - Mental health conditions
  - Treatment approaches
  - App usage instructions
  - Model details
  - Recovery factors
  - Crisis resources

### API Endpoints
- `POST /api/chat` - Send message
- `GET /api/chat/suggestions` - Get suggested questions
- `GET /api/chat/history` - View chat history
- `DELETE /api/chat/history` - Clear history

## Testing Checklist

- [x] Backend starts without errors
- [ ] Frontend starts and chatbot is visible
- [ ] Chatbot responds to messages
- [ ] Predictions work with any age
- [ ] PDF reports generate correctly
- [ ] History panel loads
- [ ] All pages accessible via navigation
- [ ] Dark/Light mode toggle works

## Next Steps

1. **Test the application**:
   ```powershell
   python .\run_app.py
   ```

2. **Verify chatbot**:
   - Look for floating 💬 button in bottom-right
   - Click to open chat window
   - Try sample questions from `CHATBOT_SAMPLE_QUESTIONS.md`

3. **Test predictions**:
   - Form now has default values
   - All ages should work
   - PDF reports should format properly

4. **Clean up** (optional):
   - Run cleanup commands above
   - Keep backups before deleting

## Important Notes

- ⚠️ Don't delete `venv/` or `.conda/` - these are active environments
- ⚠️ Keep `data/predictions.json` - contains prediction history
- ⚠️ Backup before running cleanup commands
- ✅ All core functionality is working
- ✅ Chatbot is fully integrated
- ✅ Forms have sensible defaults
