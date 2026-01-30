"""
Orchestrator Service
Manages the multi-agent audit pipeline: Inspector -> Analyst -> Advisor
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import asyncio


class AuditStatus(str, Enum):
    PENDING = "pending"
    INSPECTING = "inspecting"
    ANALYZING = "analyzing"
    ADVISING = "advising"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class InspectorOutput:
    """Output from Inspector agent (vision analysis)"""
    design_map: Dict[str, Any]  # Structured JSON map of design
    elements: list  # List of detected UI elements
    colors: Dict[str, str]  # Hex color palette
    text_content: list  # Extracted text


@dataclass
class AnalystOutput:
    """Output from Analyst agent (rule-based violations)"""
    violations: list  # List of detected violations
    categories: Dict[str, list]  # Violations grouped by category
    priority_scores: Dict[str, str]  # Critical, High, Medium, Low


@dataclass
class AdvisorOutput:
    """Output from Advisor agent (human-readable feedback)"""
    summary: str  # High-level overview
    detailed_feedback: str  # Comprehensive recommendations
    improvements: list  # Suggested improvements
    resources: list  # Links to design resources


class AuditOrchestrator:
    """
    Orchestrates the multi-agent audit pipeline.
    Responsible for:
    - Receiving user uploads
    - Routing through Inspector -> Analyst -> Advisor
    - Managing state throughout the pipeline
    - Storing results in database
    """

    def __init__(self):
        self.status = AuditStatus.PENDING
        self.inspector_output: Optional[InspectorOutput] = None
        self.analyst_output: Optional[AnalystOutput] = None
        self.advisor_output: Optional[AdvisorOutput] = None

    async def run_audit(self, image_path: str, image_url: str) -> Dict[str, Any]:
        """
        Execute the full audit pipeline for a design image.
        
        Args:
            image_path: Local file path to the uploaded image
            image_url: Cloud storage URL for the image
            
        Returns:
            Complete audit result with all agent outputs
        """
        try:
            # Step 1: Inspector Agent (Vision Analysis)
            self.status = AuditStatus.INSPECTING
            self.inspector_output = await self._run_inspector(image_url)
            
            # Step 2: Analyst Agent (Rule-Based Violation Detection)
            self.status = AuditStatus.ANALYZING
            self.analyst_output = await self._run_analyst(self.inspector_output)
            
            # Step 3: Advisor Agent (LLM-Generated Feedback)
            self.status = AuditStatus.ADVISING
            self.advisor_output = await self._run_advisor(
                self.inspector_output,
                self.analyst_output
            )
            
            self.status = AuditStatus.COMPLETED
            
            return {
                "status": self.status.value,
                "inspector": self._serialize(self.inspector_output),
                "analyst": self._serialize(self.analyst_output),
                "advisor": self._serialize(self.advisor_output),
            }
            
        except Exception as e:
            self.status = AuditStatus.FAILED
            return {
                "status": self.status.value,
                "error": str(e)
            }

    async def _run_inspector(self, image_url: str) -> InspectorOutput:
        """
        Run Inspector agent: Computer vision analysis of the design.
        """
        from agents.inspector.vision_analyzer import VisionAnalyzer
        analyzer = VisionAnalyzer()
        design_map = await analyzer.analyze(image_url)
        
        return InspectorOutput(
            design_map=design_map,
            elements=design_map.get("components", []),
            colors=design_map.get("color_palette", {}),
            text_content=design_map.get("text_content", []),
        )

    async def _run_analyst(self, inspector_output: InspectorOutput) -> AnalystOutput:
        """
        Run Analyst agent: Rules-based violation detection.
        """
        from agents.analyst.rules_engine import RulesEngine
        engine = RulesEngine()
        violations_data = engine.analyze(inspector_output.design_map)
        
        return AnalystOutput(
            violations=violations_data.get("by_severity", {}).get("critical", [])
                      + violations_data.get("by_severity", {}).get("high", [])
                      + violations_data.get("by_severity", {}).get("medium", [])
                      + violations_data.get("by_severity", {}).get("low", []),
            categories=violations_data.get("by_category", {}),
            priority_scores=violations_data.get("by_severity", {}),
        )

    async def _run_advisor(
        self,
        inspector_output: InspectorOutput,
        analyst_output: AnalystOutput
    ) -> AdvisorOutput:
        """
        Run Advisor agent: LLM-based feedback synthesis.
        """
        from agents.advisor.feedback_generator import FeedbackGenerator
        generator = FeedbackGenerator()
        
        # Prepare data for advisor
        violations_dict = {
            "total_violations": len(analyst_output.violations),
            "violations": analyst_output.violations,
            "by_category": analyst_output.categories,
        }
        
        feedback = await generator.generate_feedback(
            inspector_output.design_map,
            violations_dict
        )
        
        return AdvisorOutput(
            summary=feedback.get("summary", ""),
            detailed_feedback=feedback.get("detailed_feedback", ""),
            improvements=feedback.get("improvements", []),
            resources=feedback.get("resources", []),
        )

    def _serialize(self, obj) -> Dict[str, Any]:
        """Convert dataclass to dictionary for JSON serialization"""
        if obj is None:
            return {}
        if isinstance(obj, (InspectorOutput, AnalystOutput, AdvisorOutput)):
            return obj.__dict__
        return obj if isinstance(obj, dict) else {}
