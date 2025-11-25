from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class ClassPrediction(str, Enum):
    """Énumération des classes de prédiction"""

    NORMAL = "normal"
    BENIGN = "benign"
    MALIGNANT = "malignant"


class UrgencyLevel(str, Enum):
    """Niveau d'urgence de la consultation"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PredictionRequest(BaseModel):
    """Requête de prédiction"""

    image_base64: str = Field(..., description="Image en format base64", min_length=100)
    user_id: Optional[str] = Field(None, description="ID de l'utilisateur (optionnel)")
    cycle_day: Optional[int] = Field(
        None, ge=1, le=35, description="Jour du cycle menstruel (1-35)"
    )

    @validator("image_base64")
    def validate_base64(cls, v):
        """Valider le format base64"""
        if not v.startswith("data:image"):
            raise ValueError("Format base64 invalide")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
                "user_id": "user_123",
                "cycle_day": 14,
            }
        }


class PredictionResult(BaseModel):
    """Résultat de la prédiction"""

    prediction_id: str = Field(..., description="ID unique de la prédiction")
    timestamp: datetime = Field(..., description="Date et heure de la prédiction")

    # Résultats du modèle CV
    class_prediction: ClassPrediction = Field(..., description="Classe prédite")
    confidence: float = Field(..., ge=0, le=1, description="Confiance (0-1)")
    probabilities: Dict[str, float] = Field(
        ..., description="Probabilités pour chaque classe"
    )

    # Analyse LLM
    llm_analysis: str = Field(..., description="Analyse textuelle du LLM")
    recommendations: List[str] = Field(..., description="Liste des recommandations")
    urgency_level: UrgencyLevel = Field(..., description="Niveau d'urgence")

    # Métadonnées
    processing_time_ms: float = Field(..., description="Temps de traitement (ms)")
    model_version: str = Field(..., description="Version du modèle")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction_id": "pred_123456",
                "timestamp": "2025-01-15T10:30:00",
                "class_prediction": "normal",
                "confidence": 0.95,
                "probabilities": {"normal": 0.95, "benign": 0.03, "malignant": 0.02},
                "llm_analysis": "L'analyse montre des résultats normaux...",
                "recommendations": [
                    "Continuez vos auto-examens mensuels",
                    "Planifiez votre prochain examen de routine",
                ],
                "urgency_level": "low",
                "processing_time_ms": 1234.56,
                "model_version": "1.0.0",
            }
        }


class PredictionResponse(BaseModel):
    """Réponse de l'API"""

    success: bool = Field(..., description="Statut de la requête")
    data: Optional[PredictionResult] = Field(
        None, description="Données de prédiction (si succès)"
    )
    error: Optional[str] = Field(None, description="Message d'erreur (si échec)")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "prediction_id": "pred_123456",
                    # ... (reste de l'exemple)
                },
                "error": None,
            }
        }
