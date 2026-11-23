
Creative Intelligence AI
AI-Powered Advertisement Performance & Design Intelligence Platform

Creative Intelligence AI is an AI-powered platform that analyzes advertisement creatives using Computer Vision, Machine Learning, and Explainable AI techniques.

It combines visual design analysis with campaign conversion estimation through an interactive Streamlit dashboard and FastAPI backend.

## Key Features

- **Advertisement Image Analysis:** Upload and analyze JPG, PNG, and WEBP advertisements.
- **Computer Vision:** Evaluate brightness, contrast, resolution, and visual design characteristics.
- **Colour Diversity Analysis:** Measure colour diversity in advertisement creatives.
- **Saliency Analysis:** Generate algorithmic visual saliency statistics to identify visually prominent regions.
- **Machine Learning:** Estimate campaign conversions using a Random Forest regression pipeline.
- **Explainable AI:** Use SHAP to understand feature contributions to model predictions.
- **Batch Analysis:** Analyze multiple advertisement creatives.
- **Interactive Dashboard:** Explore results through Streamlit and Plotly visualizations.
- **Report Generation:** Download analysis reports in CSV and PDF formats.
- **REST API:** Process and analyze uploaded images through FastAPI.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn, Random Forest |
| Explainable AI | SHAP |
| Computer Vision | OpenCV |
| Backend | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Visualization | Matplotlib, Seaborn, Plotly |
| Testing | Pytest |
| Reports | ReportLab |
| Version Control | Git, GitHub |

## Project Architecture

```text
Creative-Intelligence-AI/
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample_ads/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_computer_vision.ipynb
│
├── src/
│   ├── features/
│   │   └── computer_vision.py
│   ├── models/
│   └── visualization/
│
├── models/
│   └── random_forest_pipeline.joblib
│
├── reports/
├── tests/
│   └── test_backend.py
│
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/bhawna007/creative-intelligence-ai.git
cd creative-intelligence-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the Application

The project uses a FastAPI backend and Streamlit frontend. Run them in separate terminals.

### Terminal 1 — Start FastAPI

```bash
python -m uvicorn backend.main:app --reload
```

Backend:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### Terminal 2 — Start Streamlit

```bash
python -m streamlit run frontend/app.py
```

Open the local Streamlit URL displayed in your terminal.

## Machine Learning Model

The project uses a Random Forest Regressor to estimate `Total_Conversion` from campaign-related features.

Model configuration:

- Algorithm: Random Forest Regressor
- Number of estimators: 200
- Maximum depth: 8
- Random state: 42
- Train-test split: 80:20

### Model Evaluation

| Metric | Result |
|---|---:|
| MAE | 0.972 |
| RMSE | 2.029 |
| R² Score | 0.782 |

These results are from a single train-test split on a relatively small dataset. They should not be interpreted as a guarantee of real-world performance.

## Dataset

The machine learning experiments use the Clicks Conversion Tracking dataset.

Source: [Kaggle — Clicks Conversion Tracking](https://www.kaggle.com/datasets/loveall/clicks-conversion-tracking)

The model estimates campaign conversions using campaign-related inputs. It is intended for in-campaign analysis, not pre-launch CTR prediction.

## Run Automated Tests

Execute the test suite:

```bash
python -m pytest -v
```

The current backend test suite contains 8 automated tests covering:

- Root and health endpoints
- Invalid file types
- Empty uploads
- Valid image uploads
- Minimum image dimensions
- Maximum image dimensions
- Maximum upload file size

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application welcome message |
| GET | `/health` | Backend health check |
| POST | `/upload-image` | Upload and analyze an advertisement |

## Important Methodological Notes

- Design scores are heuristic indicators, not scientifically validated measures of advertising effectiveness.
- Saliency analysis is algorithmic and does not represent actual human eye-tracking measurements.
- SHAP values explain model behavior; they do not establish causal relationships.
- Conversion estimates depend on the training dataset and available campaign features.
- Model evaluation results may vary with different data splits and datasets.

## Future Improvements

- Larger and more diverse advertisement datasets.
- Stronger model validation and cross-validation.
- Advanced visual feature extraction.
- Improved explainability and model monitoring.
- Deployment with production-grade configuration.
- User authentication and persistent analysis history.

## Author

**Bhawna Kamal**

AI/ML Engineer | Computer Vision | Machine Learning | Applied AI

GitHub: [bhawna007](https://github.com/bhawna007)

---

*Built as an applied AI/ML portfolio project combining Machine Learning, Computer Vision, Explainable AI, and full-stack application development.*
