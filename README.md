#  Mental Health Recovery Prediction App

An AI-powered web application that predicts mental health recovery timelines using advanced machine learning models, with explainable AI and an intelligent chatbot assistant.


##  Features

###  Core Functionality
- **Recovery Time Prediction**: Predicts recovery time in weeks based on patient data
- **High Accuracy**: 89.15% average confidence using stacking ensemble models
- **Confidence Scoring**: Provides confidence levels and prediction intervals
- **Risk Assessment**: Identifies key risk factors and flags

###  AI Chatbot
- **Intelligent Assistant**: Answers questions about mental health and the app
- **Knowledge Base**: 5000+ words covering conditions, treatments, and usage
- **Intent Classification**: Understands user queries automatically
- **Crisis Response**: Priority handling with immediate resources
- **Conversation History**: Tracks chat exchanges
- **Always Available**: Floating button on all pages

### Explainable AI
- **RAG Engine**: Retrieval-Augmented Generation for explanations
- **Clinical Reasoning**: Evidence-based recommendations
- **Key Factors**: Detailed breakdown of prediction drivers
- **Transparency**: Clear insights into model decisions

###  Additional Features
- **History Tracking**: Search, filter, and sort predictions
- **PDF Reports**: Comprehensive clinical documentation
- **CSV Upload**: Batch predictions from files
- **Dark Mode**: Toggle between themes
- **Responsive Design**: Works on all devices

##  Architecture

### Technology Stack

**Backend:**
- FastAPI (Python 3.9+)
- Scikit-learn (ML models)
- XGBoost, LightGBM, CatBoost
- Pydantic (validation)
- Uvicorn (ASGI server)

**Frontend:**
- React 18
- Vite (build tool)
- TailwindCSS
- React Router

**ML Model:**
- Stacking Ensemble
- 30+ engineered features
- Training data: 4000+ samples

##  Getting Started

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- Conda (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd mental-health-recovery-app
```

2. **Set up Python environment**
```powershell
# Using Conda
conda create -n mental-health python=3.9
conda activate mental-health

# Install dependencies
pip install -r backend/requirements.txt
```

3. **Set up Frontend**
```powershell
cd mental-health-frontend
npm install
cd ..
```

4. **Run the application**
```powershell
# Single command to start both backend and frontend
python run_app.py
```

5. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

##  Usage

### Making Predictions

1. Navigate to the "Predict" page
2. Fill in patient information:
   - Demographics (age, gender, education)
   - Clinical data (diagnosis, severity, comorbidities)
   - Treatment details (medication, therapy, sessions)
   - Social factors (support, living situation)
3. Click "Get Prediction"
4. View results with confidence score and risk flags
5. Click "Explain with AI" for detailed insights

### Using the Chatbot

1. Look for the button in the bottom-right corner
2. Click to open the chat window
3. Ask questions like:
   - "What is this app about?"
   - "How does the prediction model work?"
   - "Tell me about depression treatment"
   - "How do I generate a PDF report?"
4. Use suggested questions for guidance
5. Get instant responses with clinical references

See `CHATBOT_SAMPLE_QUESTIONS.md` for 75+ example questions!

### Viewing History

1. Open the History Panel (sidebar)
2. Search by diagnosis
3. Filter by severity (High/Medium/Low)
4. Sort by newest or oldest
5. Click any record to view details

### Generating Reports

1. Make a prediction or view from history
2. Click "Download Report"
3. PDF includes:
   - Prediction summary
   - Patient inputs (formatted table)
   - Interpretation
   - Model confidence

### CSV Upload

1. Navigate to CSV Upload section
2. Prepare CSV with required columns
3. Upload file for batch predictions
4. Download results CSV

##  API Endpoints

### Predictions
- `POST /api/predict` - Submit prediction request
- `GET /api/history` - Retrieve prediction history
- `GET /api/report/{id}` - Generate PDF report
- `POST /api/upload` - CSV batch upload
- `POST /api/explain` - Get AI explanation

### Chatbot (NEW!)
- `POST /api/chat` - Send message to chatbot
- `GET /api/chat/suggestions` - Get suggested questions
- `GET /api/chat/history` - View conversation history
- `DELETE /api/chat/history` - Clear chat history

##  Model Information

### Stacking Ensemble Architecture
- **Base Models**:
  - XGBoost: Gradient boosting for structured data
  - LightGBM: Fast, efficient gradient boosting
  - CatBoost: Handles categorical features natively
- **Meta-Learner**: Combines base model predictions

### Performance Metrics
- Average Confidence: 89.15%
- Features: 30+ engineered features
- Training Data: 4000+ synthetic patient records
- Validation: Cross-validated

### Input Parameters (30+ features)
- **Demographics**: Age, Gender, Education, Employment
- **Clinical**: Diagnosis, Severity, Comorbidities, History
- **Treatment**: Medication, Therapy Type, Session Frequency
- **Social**: Support Level, Living Situation, Income
- **Lifestyle**: (derived features)

##  Development

### Project Structure
```
mental-health-recovery-app/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── config.py     # Configuration
│   │   └── main.py       # FastAPI app
│   ├── data/             # Knowledge bases
│   ├── ml_models/        # Trained models
│   └── requirements.txt
├── mental-health-frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── context/      # React context
│   │   ├── utils/        # Utilities
│   │   └── App.jsx       # Main app
│   └── package.json
├── CHATBOT_SAMPLE_QUESTIONS.md
├── CLEANUP_GUIDE.md
├── README.md
└── run_app.py
```

---

**Built with ❤️ for better mental health care**

