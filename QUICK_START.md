# 🚀 Quick Start Guide - Mental Health Recovery App

## Issues Fixed ✅

### 1. Age Validation Error (422 Error)
**Problem**: Backend rejected age values < 18
**Solution**: Updated `backend/app/models/schemas.py` to accept ages 0-120

### 2. Missing Chatbot
**Problem**: Chatbot component not visible
**Solution**: Moved chatbot to main App component in `App.jsx`

### 3. Empty Form Errors
**Problem**: Form submitted empty values causing validation errors
**Solution**: Added sensible default values to `PredictionForm.jsx`

## How to Start the App

### Option 1: Using run_app.py (Recommended)
```powershell
python .\run_app.py
```
This starts both backend and frontend in separate windows.

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd mental-health-frontend
npm run dev
```

## Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Finding the Chatbot 💬

1. Start the application
2. Look at the **bottom-right corner** of any page
3. You'll see a **floating purple button with 💬**
4. Click it to open the chat window
5. Try asking: "What is this app about?"

## Testing the Fixes

### Test 1: Age Validation
1. Go to http://localhost:5173/predict
2. The form will have default values (age: 25)
3. Try changing age to any value (even 5 or 100)
4. Click "Get Prediction"
5. ✅ Should work without 422 errors

### Test 2: Chatbot
1. Look for 💬 button in bottom-right
2. Click to open chat
3. Type "Hello!"
4. ✅ Should get a welcome message
5. Try "What is depression?"
6. ✅ Should get detailed information

### Test 3: Predictions
1. Leave default values or modify them
2. Click "Get Prediction"
3. ✅ Should see results with confidence score
4. Click "Explain with AI"
5. ✅ Should see detailed explanation

### Test 4: History
1. After making predictions, click "History" in navigation
2. ✅ Should see list of past predictions
3. Try search and filters
4. Click a record to view details

### Test 5: PDF Report
1. Make a prediction
2. Click "Download Report"
3. ✅ Should download PDF with formatted table

## Sample Chatbot Questions

Quick test questions:
1. "Hello!"
2. "What is this app about?"
3. "How does the prediction model work?"
4. "What is depression?"
5. "How do I generate a PDF report?"
6. "What should I do in a crisis?"
7. "How accurate are predictions?"
8. "Tell me about anxiety treatment"
9. "What factors affect recovery?"
10. "How do I view my history?"

See `CHATBOT_SAMPLE_QUESTIONS.md` for 75+ more questions!

## Common Issues & Solutions

### Backend Error: "Module not found"
```powershell
# Ensure you're in the right environment
conda activate mental-health

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Frontend Error: "Cannot find module"
```powershell
cd mental-health-frontend
rm -r node_modules
npm install
```

### Chatbot Not Visible
1. Open browser console (F12)
2. Look for errors
3. Check that you're on http://localhost:5173
4. Try hard refresh (Ctrl + Shift + R)

### Port Already in Use
```powershell
# Kill processes on port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Kill processes on port 5173
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process
```

## Features Tour

### 1. Home Page
- Welcome screen
- Navigation to Predict and History
- Chatbot available in corner

### 2. Predict Page
- **Pre-filled Form**: Default values to prevent errors
- **All Fields**: Demographics, clinical, treatment data
- **Submit**: Get prediction instantly
- **Results**: Confidence score, risk flags, interpretation
- **Explain AI**: Detailed RAG explanation
- **Download Report**: PDF generation

### 3. History Page
- **Search**: Filter by diagnosis
- **Severity Filter**: High/Medium/Low
- **Sort**: Newest/Oldest first
- **Click Record**: View full details
- **Sidebar**: Always accessible

### 4. Chatbot (All Pages)
- **Floating Button**: Bottom-right corner (💬)
- **Smart Responses**: Intent classification
- **Knowledge Base**: 5000+ words
- **Crisis Priority**: Immediate emergency resources
- **Suggestions**: Helpful question prompts
- **History**: Maintains conversation context
- **Formatting**: Markdown support

## What's New in v2.0

✨ **AI Chatbot Integration**
- Comprehensive knowledge base
- Intent classification
- RAG capabilities
- Crisis response
- Suggested questions

🐛 **Bug Fixes**
- Age validation (now 0-120 years)
- Default form values
- Chatbot visibility
- PDF formatting

🎨 **UI Improvements**
- Better form UX
- Consistent styling
- Dark mode support
- Responsive design

## Next Steps

1. **Explore Features**: Try all pages and features
2. **Test Chatbot**: Ask various questions
3. **Make Predictions**: Test with different patient data
4. **Review History**: Check past predictions
5. **Generate Reports**: Download PDF reports
6. **Read Documentation**: Check `README.md` for details

## Getting Help

- **Chatbot**: Ask the AI assistant
- **Sample Questions**: `CHATBOT_SAMPLE_QUESTIONS.md`
- **Cleanup Guide**: `CLEANUP_GUIDE.md`
- **API Docs**: http://localhost:8000/docs
- **README**: Full documentation

## Development Tips

### Hot Reload
Both backend and frontend have hot reload:
- **Backend**: Uvicorn watches for file changes
- **Frontend**: Vite hot module replacement

### Adding Features
1. **Backend API**: Add to `backend/app/api/`
2. **Frontend Component**: Add to `src/components/`
3. **API Client**: Update `src/utils/api.js`
4. **Routes**: Register in `backend/app/main.py`

### Debugging
- **Backend Logs**: Check terminal running uvicorn
- **Frontend Console**: F12 → Console tab
- **Network**: F12 → Network tab
- **API Docs**: Test endpoints at `/docs`

## Performance Tips

- First load might be slow (model loading)
- Subsequent predictions are fast
- Chatbot responses are instant
- PDF generation takes 2-3 seconds

## Security Notes

- All data stored locally in `predictions.json`
- No external API calls except OpenAI (if configured)
- CORS enabled for development
- Use HTTPS in production

## Cleanup (Optional)

To remove unnecessary files:
```powershell
# See CLEANUP_GUIDE.md for details
Remove-Item -Recurse -Force .\backend\oldenv
Remove-Item -Recurse -Force .\backend\oldenv39
Remove-Item -Recurse -Force .\old_scripts
```

---

**You're all set! 🎉**

The app is now fully functional with:
- ✅ Working predictions (all ages)
- ✅ Visible chatbot (💬 button)
- ✅ Default form values
- ✅ Comprehensive knowledge base
- ✅ PDF reports with formatting
- ✅ Complete history tracking

**Enjoy exploring your Mental Health Recovery App!** 🧠
