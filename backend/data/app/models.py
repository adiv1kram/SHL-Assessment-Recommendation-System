from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    """
    Request model for the recommendation endpoint.
    Strictly follows Appendix 2[cite: 169].
    """
    query: str = Field(..., description="The natural language query or job description text")

class AssessmentItem(BaseModel):
    """
    Represents a single assessment recommendation.
    Fields match the 'Response Fields Explanation' table exactly[cite: 183].
    """
    url: str = Field(..., description="Valid URL to the assessment resource")
    name: str = Field(..., description="Name of the assessment")
    adaptive_support: str = Field(..., pattern="^(Yes|No)$", description="Either 'Yes' or 'No'")
    description: str = Field(..., description="Detailed description of the assessment")
    duration: int = Field(..., description="Duration of the assessment in minutes")
    remote_support: str = Field(..., pattern="^(Yes|No)$", description="Either 'Yes' or 'No'")
    test_type: List[str] = Field(..., description="Categories or types of the assessment")

class RecommendationResponse(BaseModel):
    """
    Wrapper for the list of recommendations.
    """
    recommended_assessments: List[AssessmentItem]