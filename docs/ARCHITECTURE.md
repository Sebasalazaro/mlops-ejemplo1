# Architecture Documentation

## System Overview

This MLOps pipeline implements an automated deployment system for machine learning models. The architecture follows a GitOps approach where code changes trigger automated build and deployment processes.

## Components

### 1. Training Pipeline (Local)

**Location**: `src/train.py`

The training component runs locally on a data scientist's workstation and performs:

- **Data Loading**: Loads the Iris dataset from scikit-learn
- **Data Splitting**: 80/20 train-test split with configurable random state
- **Feature Engineering**: Creates preprocessing pipelines for numerical features
  - StandardScaler for normalization
  - VarianceThreshold for feature selection
- **Model Training**: Trains a DummyClassifier (baseline model)
- **Artifact Generation**: Saves two pickle files:
  - `transformer.pickle`: Feature preprocessing pipeline
  - `model.pickle`: Trained classification model

**Technology Stack**:
- scikit-learn 1.1.2
- pandas 1.4.4
- Python 3.9

### 2. REST API (Cloud Deployed)

**Location**: `api/api.py`

FastAPI application that serves predictions through HTTP endpoints:

**Endpoints**:
- `GET /`: API information and status
- `GET /get-iris-type`: Prediction endpoint accepting 4 flower measurements
- `GET /health`: Health check for monitoring

**Request Flow**:
1. Client sends HTTP GET request with query parameters
2. API validates input parameters
3. Creates pandas DataFrame with proper feature names
4. Applies transformer for feature preprocessing
5. Model generates prediction
6. Returns JSON response with predicted class

**Technology Stack**:
- FastAPI 0.82.0
- Uvicorn 0.18.3 (ASGI server)
- Python 3.9

### 3. Configuration Management

**Location**: `config/settings.py`

Centralized configuration module providing:
- Environment variable management with defaults
- Path configuration for models and outputs
- API server settings
- Training hyperparameters

**Design Pattern**: Configuration as code with environment variable override capability

### 4. Container Image

**Location**: `Dockerfile`

Multi-stage Docker build process:

1. Base image: `tiangolo/uvicorn-gunicorn-fastapi:python3.9`
2. Install Python dependencies from `requirements.txt`
3. Copy application code and configuration
4. Copy model artifacts
5. Expose port 8080
6. Set uvicorn as entrypoint

**Image Characteristics**:
- Stateless container design
- Model artifacts baked into image
- Production-ready with gunicorn workers
- Health check compatible

### 5. CI/CD Pipeline

**Location**: `cloudbuild.yaml`

Google Cloud Build configuration with three steps:

**Step 1: Build**
```bash
docker build -t gcr.io/[PROJECT-ID]/mlops-ejemplo1 .
```
Creates container image from Dockerfile

**Step 2: Push**
```bash
docker push gcr.io/[PROJECT-ID]/mlops-ejemplo1
```
Uploads image to Google Container Registry

**Step 3: Deploy**
```bash
gcloud run deploy mlops-ejemplo1 \
  --image=gcr.io/[PROJECT-ID]/mlops-ejemplo1 \
  --region=us-central1 \
  --platform=managed
```
Deploys container to Cloud Run serverless platform

**Triggers**: Automatically runs on push to `main` branch

## Data Flow

### Training Flow

```
┌──────────────────┐
│ Iris Dataset     │
│ (scikit-learn)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Train/Test Split │
│ (80/20)          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Feature Pipeline │
│ - Scaling        │
│ - Selection      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Model Training   │
│ (DummyClassifier)│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Save Artifacts   │
│ - transformer    │
│ - model          │
└──────────────────┘
```

### Prediction Flow

```
┌──────────────────┐
│ HTTP Request     │
│ /get-iris-type   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Input Validation │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Load Transformer │
│ & Model          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Preprocess Input │
│ (transformer)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Generate         │
│ Prediction       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Return JSON      │
│ Response         │
└──────────────────┘
```

### Deployment Flow

```
┌──────────────────┐
│ Developer        │
│ git push         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ GitHub           │
│ Repository       │
└────────┬─────────┘
         │ webhook
         ▼
┌──────────────────┐
│ Cloud Build      │
│ Trigger          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Build Container  │
│ (Docker)         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Container        │
│ Registry (GCR)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Cloud Run        │
│ Deploy           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Live API         │
│ Endpoint         │
└──────────────────┘
```

## Design Decisions

### Why DummyClassifier?

The project uses `DummyClassifier` as a baseline model to:
- Establish performance baseline for future model iterations
- Demonstrate the deployment pipeline with minimal complexity
- Focus on MLOps infrastructure rather than model sophistication

In production, this would be replaced with more sophisticated algorithms (Random Forest, Gradient Boosting, Neural Networks).

### Why Pickle Model Storage?

**Pros**:
- Simple serialization for quick prototyping
- Native scikit-learn support
- Small file size for simple models

**Cons**:
- Security concerns (pickle can execute arbitrary code)
- Not version-controlled effectively
- Difficult to inspect model metadata

**Production Alternative**: Use MLflow Model Registry or similar model versioning system.

### Why Cloud Run?

**Advantages**:
- Serverless: No infrastructure management
- Auto-scaling: Scales to zero when not in use
- Cost-effective: Pay only for actual usage
- Fast deployment: Seconds to deploy new versions
- Built-in HTTPS and custom domains

**Trade-offs**:
- Cold start latency for first request
- Limited to HTTP/HTTPS protocols
- Maximum request timeout constraints

### Stateless API Design

The API is designed to be completely stateless:
- No session storage
- No in-memory caching
- Model loaded at startup (not per-request)

This enables:
- Horizontal scaling without sticky sessions
- Easy rollback to previous versions
- Simplified debugging and testing

## Security Considerations

### Current Implementation

1. **Model Artifacts**: Baked into container image
2. **Environment Variables**: Configurable through Cloud Run
3. **Network**: HTTPS by default on Cloud Run
4. **Authentication**: None (public API)

### Production Recommendations

1. **API Security**:
   - Implement API key authentication
   - Add rate limiting
   - Enable CORS with whitelist
   - Use Cloud Armor for DDoS protection

2. **Model Security**:
   - Store models in Cloud Storage with IAM controls
   - Implement model signing for integrity verification
   - Encrypt models at rest

3. **Network Security**:
   - Use VPC connector for private resources
   - Implement Cloud Endpoints for API management
   - Enable Cloud Audit Logs

## Scalability

### Current Capacity

Cloud Run configuration:
- **Concurrency**: 80 requests per container (default)
- **Memory**: 256MB (configurable)
- **CPU**: 1 vCPU (configurable)
- **Instances**: Auto-scaling from 0 to 100

### Bottlenecks

1. **Model Loading**: Happens at container startup (cold start)
2. **Transformer Overhead**: Feature preprocessing on every request
3. **Pickle Deserialization**: Not optimized for high throughput

### Optimization Strategies

1. **Reduce Cold Starts**:
   - Minimum instances configuration
   - Smaller container image
   - Lazy loading of dependencies

2. **Improve Throughput**:
   - Batch prediction support
   - Request caching for common inputs
   - Model optimization (ONNX, TensorRT)

3. **Horizontal Scaling**:
   - Load balancing across regions
   - Read replicas for model artifacts
   - CDN for static assets

## Monitoring and Observability

### Current Implementation

- Health check endpoint (`/health`)
- Cloud Logging integration
- Basic FastAPI exception handling

### Production Requirements

1. **Metrics**:
   - Request latency (p50, p95, p99)
   - Error rates by endpoint
   - Prediction distribution
   - Model inference time

2. **Logging**:
   - Structured JSON logs
   - Request/response logging
   - Model version tracking
   - Failed prediction logging

3. **Alerting**:
   - High error rate alerts
   - Latency degradation
   - Anomalous prediction patterns
   - Container crash alerts

4. **Tracing**:
   - End-to-end request tracing
   - Model inference profiling
   - Dependency latency tracking

## Future Enhancements

### Model Improvements

1. Replace DummyClassifier with production-grade models
2. Implement A/B testing framework
3. Add model versioning and rollback capabilities
4. Continuous training pipeline

### Infrastructure

1. Multi-region deployment
2. Database integration for prediction logging
3. Feature store for real-time features
4. Model serving optimization (TF Serving, Seldon)

### MLOps Maturity

1. Automated model evaluation and approval
2. Data drift detection
3. Model performance monitoring
4. Automated retraining triggers
5. Shadow deployments for validation

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [scikit-learn Pipeline Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
- [12-Factor App Methodology](https://12factor.net/)
