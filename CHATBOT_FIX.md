# Chatbot Domain Restriction Fix

## Issue
Chatbot was rejecting valid mental health questions like:
- "How can I recover from Depression?"
- "Tell me all you know about General wellness"
- "Talk to me about depression"

## Root Cause
Domain validation was too strict:
- Threshold: 0.6 (60%) confidence required
- Limited keyword matching
- Didn't boost obvious mental health queries

## Fixes Applied ✅

### 1. Lowered Threshold (chatbot_engine.py line ~130)
**Before**: `is_valid = final_score >= 0.6` (60% required)
**After**: `is_valid = final_score >= 0.3` (30% required)

### 2. Added Mental Health Boost (chatbot_engine.py line ~125)
```python
mental_health_terms = ['depression', 'anxiety', 'wellness', 'mental health', 
                       'recovery', 'stress', 'therapy', 'counseling', 'help', 
                       'support', 'cope', 'coping']
if any(term in query_lower for term in mental_health_terms):
    final_score = max(final_score, 0.7)  # Auto-accept mental health queries
```

### 3. Extended Allowed Domains (chatbot_engine.py line ~20)
Added keywords:
- 'recover', 'healing', 'health', 'help'
- 'feel', 'feeling', 'sad', 'worried'
- 'general', 'cope', 'talk', 'listen'
- 'understand', 'improve', 'better'

### 4. Homepage Button Fix (Home.jsx)
**Removed**: "Start Your Journey" button
**Kept**: "Recovery Assessment" button with gradient styling

---

## Test Results (Expected)

### These Should Now Work:
✅ "How can I recover from Depression?" → Score: 0.7+ (mental health boost)
✅ "Tell me all you know about General wellness" → Score: 0.7+ (wellness keyword)
✅ "Talk to me about depression" → Score: 0.7+ (depression keyword)
✅ "I feel sad" → Score: 0.7+ (feel + sad keywords)
✅ "How to cope with stress?" → Score: 0.7+ (cope + stress keywords)
✅ "What is anxiety?" → Score: 0.7+ (anxiety keyword)

### These Should Still Be Rejected:
❌ "What's the weather?" → Score: ~0.0 (rejection keyword)
❌ "Who won the game?" → Score: ~0.1 (no mental health terms)
❌ "Tell me a joke" → Score: ~0.1 (no mental health terms)

---

## How to Test

1. **Restart Backend**:
   ```powershell
   # Stop current backend (Ctrl+C)
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Test Chatbot**:
   - Open app: http://localhost:5173
   - Click chatbot icon (bottom right)
   - Try these questions:
     - "How can I recover from Depression?"
     - "Tell me about general wellness"
     - "I feel anxious, what should I do?"
   - All should get helpful responses (not rejection)

3. **Check Homepage**:
   - Open: http://localhost:5173
   - Should see ONE button: "Recovery Assessment" (gradient style)
   - No "Start Your Journey" button

---

## Technical Details

### Scoring System (Updated)
- **Keyword Match (30%)**: Query contains allowed domain keywords
- **KB Overlap (50%)**: Query words overlap with knowledge base
- **Pattern Match (20%)**: Matches mental health question patterns
- **Mental Health Boost**: Auto-sets score to 0.7 if mental health term detected

### Threshold Logic
```
if final_score >= 0.3:  # 30% threshold (was 60%)
    accept_query()
else:
    reject_query()
```

### Mental Health Boost Logic
```
if 'depression' in query OR 'wellness' in query OR 'anxiety' in query:
    final_score = max(final_score, 0.7)  # Override low scores
```

---

## Files Changed
1. `backend/app/services/chatbot_engine.py` - Lines ~20, ~125-135
2. `mental-health-frontend/src/components/Home.jsx` - Lines ~80-90

---

## Impact
- **More Natural**: Users can ask mental health questions naturally
- **Less Frustrating**: Won't reject valid health-related queries
- **Still Protected**: Weather, sports, politics still rejected
- **Better UX**: Cleaner homepage with single CTA button

---

**Status**: Fixed. Restart backend and test the chatbot with mental health questions.
