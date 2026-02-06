<div align="center">

# MLOps Iris Classification Pipeline

Automated machine learning deployment pipeline for Iris flower classification using FastAPI and Google Cloud Platform. This project demonstrates end-to-end MLOps practices including model training, containerization, and automated CI/CD deployment.

<br/>

![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white) ![Cloud Build](https://img.shields.io/badge/Cloud_Build-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white) ![Cloud Run](https://img.shields.io/badge/Cloud_Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

</div>

## 📋 Overview

This project implements a complete MLOps workflow that automatically deploys a machine learning model to production. The pipeline trains an Iris species classifier locally and exposes it through a REST API deployed on Google Cloud Platform using automated CI/CD practices.

**Key Features:**
- Automated model training with preprocessing pipelines
- RESTful API for real-time predictions
- Containerized deployment with Docker
- CI/CD automation using GCP Cloud Build
- Infrastructure as code for reproducible deployments
- Health monitoring and error handling

## 🏗️ Architecture

```
┌─────────────────┐
│  Local Training │
│   (train.py)    │
└────────┬────────┘
         │ generates
         ▼
┌─────────────────┐
│ Model Artifacts │
│  (*.pickle)     │
└────────┬────────┘
         │
         │ git push
         ▼
┌─────────────────┐      ┌──────────────┐      ┌─────────────┐
│     GitHub      │─────▶│ Cloud Build  │─────▶│  Cloud Run  │
│   Repository    │      │ (CI/CD)      │      │  (API)      │
└─────────────────┘      └──────────────┘      └─────────────┘
                              │
                              ├─ Build Docker Image
                              ├─ Push to Container Registry
                              └─ Deploy to Cloud Run
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker (optional, for local containerized testing)
- GCP account with Cloud Build and Cloud Run enabled
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mlops-ejemplo1-sebas
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional)
   ```bash
   cp config/.env.example .env
   # Edit .env with your configuration
   ```

### Training the Model

Train the classification model locally:

```bash
python src/train.py
```

This generates:
- `outputs/model.pickle` - Trained classifier
- `outputs/transformer.pickle` - Feature preprocessing pipeline

### Running the API Locally

**Option 1: Direct Python execution**
```bash
python run_api.py
```

**Option 2: Using Docker**
```bash
docker build -t iris-api .
docker run -p 8080:8080 iris-api
```

**Option 3: Using Docker Compose**
```bash
docker-compose up
```

Access the API at `http://localhost:8080`

### Testing the API

**Using curl:**
```bash
curl "http://localhost:8080/get-iris-type?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2"
```

**Response:**
```json
[0]
```

**API Documentation:** Visit `http://localhost:8080/docs` for interactive Swagger UI

## 📁 Project Structure

```
mlops-ejemplo1-sebas/
├── api/                    # FastAPI application
│   └── api.py             # REST API endpoints
├── config/                # Configuration files
│   ├── __init__.py
│   ├── settings.py        # Application settings
│   └── .env.example       # Environment template
├── docs/                  # Documentation
│   └── ARCHITECTURE.md    # Detailed architecture
├── outputs/               # Model artifacts (generated)
│   ├── model.pickle       # Trained model
│   └── transformer.pickle # Preprocessing pipeline
├── src/                   # Source code
│   └── train.py          # Model training script
├── cloudbuild.yaml       # GCP Cloud Build configuration
├── docker-compose.yml    # Local Docker orchestration
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
├── run_api.py           # API startup script
└── README.md            # This file
```

## ⚙️ Configuration

Key configuration options in `config/settings.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8080` |
| `TEST_SIZE` | Train/test split ratio | `0.2` |
| `MODEL_PATH` | Path to saved model | `outputs/model.pickle` |

Environment variables can be set via `.env` file or system environment.

## 🔧 GCP Deployment

### Setup

1. **Create GCP Project**
   ```bash
   gcloud projects create your-mlops-project
   gcloud config set project your-mlops-project
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   ```

3. **Configure Cloud Build Trigger**
   - Connect your GitHub repository
   - Set trigger on `main` branch pushes
   - Use `cloudbuild.yaml` configuration

4. **Update `cloudbuild.yaml`**
   ```yaml
   # Replace with your GCP project ID
   gcr.io/YOUR-PROJECT-ID/mlops-ejemplo1
   ```

### Automated Deployment

Once configured, every push to `main` automatically:
1. Builds the Docker image
2. Pushes to Container Registry
3. Deploys to Cloud Run
4. Makes API publicly accessible

## 🧪 API Endpoints

### `GET /`
Health check and API information

### `GET /get-iris-type`
Predict Iris species from measurements

**Parameters:**
- `sepal_length` (float): Sepal length in cm
- `sepal_width` (float): Sepal width in cm
- `petal_length` (float): Petal length in cm
- `petal_width` (float): Petal width in cm

**Returns:** Array with predicted class `[0, 1, or 2]`
- 0: Setosa
- 1: Versicolor
- 2: Virginica

### `GET /health`
Service health status

## 🛠️ Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests (when test suite is added)
pytest tests/
```

### Code Quality
```bash
# Format code
black src/ api/

# Lint code
flake8 src/ api/
```

## 📚 Technologies

- **Python 3.9**: Core programming language
- **scikit-learn**: Machine learning library
- **FastAPI**: Modern web framework for APIs
- **Docker**: Containerization platform
- **Google Cloud Build**: CI/CD automation
- **Google Cloud Run**: Serverless container platform
- **Uvicorn**: ASGI server

## 🔍 MLOps Considerations

This project demonstrates several MLOps best practices:

✅ **Reproducibility**: Fixed random seeds and versioned dependencies  
✅ **Automation**: Automated CI/CD pipeline  
✅ **Containerization**: Docker for consistent environments  
✅ **API Design**: RESTful API with proper error handling  
✅ **Configuration Management**: Centralized settings  
✅ **Documentation**: Comprehensive project documentation  

⚠️ **Areas for Improvement**:
- Model versioning and registry
- Automated testing and validation
- Monitoring and logging infrastructure
- Model performance tracking over time
- A/B testing capabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Sebastian - EAFIT University
- Professor Edwin Montoya - emontoya@eafit.edu.co

## 🙏 Acknowledgments

Developed as part of the Intensive Systems course at EAFIT University (2025-2).

---

<div align="center">
Made with 🚀 for MLOps learning
</div>
