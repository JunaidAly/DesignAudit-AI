"""
Advisor Agent - LLM-Based Feedback Synthesis
Generates human-readable, constructive design feedback using GPT-4/Claude
"""
from typing import Dict, Any, Optional
import json


class FeedbackGenerator:
    """
    Uses LLM (GPT-4/Claude) to synthesize Inspector and Analyst outputs
    into human-readable, constructive feedback.
    
    Responsibilities:
    - Synthesize technical violations into plain English
    - Frame suggestions constructively and educationally
    - Provide actionable improvement steps
    - Generate priority summary and quick wins
    - Support follow-up questions via chat interface
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        # self.client = OpenAI(api_key=api_key)

    async def generate_feedback(
        self,
        design_map: Dict[str, Any],
        violations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive feedback report.
        
        Args:
            design_map: Output from Inspector agent
            violations: Output from Analyst agent
            
        Returns:
            Comprehensive feedback with summary, detailed report, and actionable items
        """
        
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_user_prompt(design_map, violations)
        
        try:
            # TODO: Call LLM API
            # response = self.client.chat.completions.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": user_prompt}
            #     ],
            #     temperature=0.7,
            #     max_tokens=2000
            # )
            # content = response.choices[0].message.content
            
            # Parse structured response
            feedback = self._parse_feedback_response(user_prompt)
            
            return {
                "status": "success",
                "summary": feedback.get("summary"),
                "detailed_feedback": feedback.get("detailed_feedback"),
                "improvements": feedback.get("improvements"),
                "quick_wins": feedback.get("quick_wins"),
                "resources": feedback.get("resources"),
                "next_steps": feedback.get("next_steps")
            }
            
        except Exception as e:
            raise Exception(f"Feedback generation failed: {str(e)}")

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the Advisor agent"""
        return """You are an expert design critic and mentor with 15+ years of experience 
in UX/UI design. Your role is to provide thoughtful, constructive feedback that helps 
junior and mid-level designers improve their work.

Key principles:
1. Be encouraging but honest - acknowledge good decisions while pointing out improvements
2. Frame all feedback educationally - explain the "why" behind each suggestion
3. Prioritize impact - focus on changes that will have the biggest positive effect
4. Be specific and actionable - provide concrete next steps, not vague criticism
5. Reference design standards - cite Material Design, Apple HCI, WCAG, industry best practices
6. Consider context - understand that design is about balance and trade-offs

Format your response as JSON with the following structure:
{
    "summary": "2-3 sentence overview of the design's strengths and main improvement areas",
    "detailed_feedback": "Comprehensive paragraph(s) discussing findings, organized by theme",
    "improvements": [
        {
            "area": "category name (e.g., Accessibility, Spacing, Typography)",
            "issue": "specific problem identified",
            "impact": "why this matters (e.g., affects 40% of users with low vision)",
            "recommendation": "concrete action to take",
            "priority": "critical|high|medium|low",
            "example": "When users tap buttons smaller than 44x44px, they often miss the target"
        }
    ],
    "quick_wins": [
        "Small changes with big impact - easy to implement today"
    ],
    "resources": [
        {
            "title": "Resource title",
            "url": "https://...",
            "type": "guide|tool|standard",
            "reason": "why this is relevant to the feedback"
        }
    ],
    "next_steps": [
        "Prioritized actions for the designer"
    ]
}"""

    def _create_user_prompt(
        self,
        design_map: Dict[str, Any],
        violations: Dict[str, Any]
    ) -> str:
        """Create the user prompt for analysis"""
        violations_summary = json.dumps(violations, indent=2)
        design_summary = self._summarize_design(design_map)
        
        return f"""Please analyze this design and provide constructive feedback.

DESIGN OVERVIEW:
{design_summary}

DETECTED ISSUES:
{violations_summary}

Based on this information:
1. Provide an honest but encouraging assessment
2. Explain the impact of key issues
3. Suggest specific, actionable improvements
4. Prioritize recommendations by impact
5. Identify quick wins - changes that are easy to implement
6. Recommend resources for learning

Remember: Frame all suggestions as opportunities to improve, not failures."""

    def _summarize_design(self, design_map: Dict[str, Any]) -> str:
        """Summarize the design for the LLM"""
        layout = design_map.get("layout", {})
        components = design_map.get("components", [])
        colors = design_map.get("color_palette", {})
        
        summary = f"""
- Viewport: {layout.get('viewport_type', 'unknown')}
- Dimensions: {layout.get('page_dimensions', {})}
- Number of components: {len(components)}
- Component types: {', '.join(set(c.get('type', 'unknown') for c in components))}
- Colors: {len(colors.get('primary', []))} primary, {len(colors.get('secondary', []))} secondary
- Key elements: {', '.join(c.get('content', '')[:30] for c in components[:3])}
"""
        return summary

    def _parse_feedback_response(self, analysis: str) -> Dict[str, Any]:
        """Parse LLM response into structured feedback"""
        # Mock implementation - return structured feedback
        return {
            "summary": "This design shows a solid foundation with good visual hierarchy and clear CTAs. The main opportunities for improvement are in accessibility (contrast ratios and touch target sizes) and spacing consistency.",
            
            "detailed_feedback": """Overall Assessment:
The design demonstrates professional execution with a cohesive color scheme and clear information architecture. The layout effectively guides users through the content, and the visual hierarchy is strong.

Key Strengths:
- Clear visual hierarchy with well-defined primary and secondary actions
- Consistent component spacing with good use of whitespace
- Professional color palette with good semantic use

Areas for Improvement:
- Accessibility: Several text elements fall below WCAG AA contrast standards
- Spacing: While generally consistent, some components deviate from the 8px grid
- Typography: The design uses 6 font sizes when 4-5 would be more cohesive""",
            
            "improvements": [
                {
                    "area": "Accessibility",
                    "issue": "Text contrast ratio 3.8:1 below WCAG AA requirement",
                    "impact": "Affects users with low vision, about 8% of population",
                    "recommendation": "Increase contrast to 4.5:1 by darkening text color from #666 to #333",
                    "priority": "high",
                    "example": "The gray button labels are hard to read for people with color vision deficiency"
                },
                {
                    "area": "Touch Targets",
                    "issue": "Several buttons are 36x36px, below 44x44px minimum",
                    "impact": "Users with motor control issues struggle to tap small targets",
                    "recommendation": "Increase all interactive elements to at least 44x44px",
                    "priority": "high",
                    "example": "Increase padding inside buttons from 8px to 12px"
                },
                {
                    "area": "Spacing",
                    "issue": "Some padding values (13px, 18px) don't align to 8px grid",
                    "impact": "Makes design less systematic and harder to scale",
                    "recommendation": "Align all spacing to 8px units: 8, 16, 24, 32, 40px",
                    "priority": "medium",
                    "example": "Change 13px padding to 16px for consistency"
                }
            ],
            
            "quick_wins": [
                "Increase button contrast from #666 on #FFF to #333 on #FFF (takes 2 minutes)",
                "Add 4px padding to buttons to reach 44x44px minimum size",
                "Standardize the two extra font sizes down to core scale",
                "Add 8px margin between form elements for better spacing"
            ],
            
            "resources": [
                {
                    "title": "WCAG 2.1 Contrast Requirements",
                    "url": "https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html",
                    "type": "standard",
                    "reason": "Understand exact contrast requirements for different text sizes"
                },
                {
                    "title": "Material Design Touch Targets",
                    "url": "https://material.io/design/usability/accessibility.html",
                    "type": "guide",
                    "reason": "Industry-standard recommendations for interactive element sizing"
                },
                {
                    "title": "8pt Grid System Guide",
                    "url": "https://builttoadapt.io/8-point-grid-units-typography-scales-and-more-966e9a8f823e",
                    "type": "guide",
                    "reason": "Learn why systematic spacing matters and how to implement it"
                }
            ],
            
            "next_steps": [
                "1. Fix high-priority contrast issues (30 mins) - biggest accessibility impact",
                "2. Increase all touch targets to 44x44px minimum (30 mins)",
                "3. Align spacing to 8px grid system (1 hour)",
                "4. Consolidate font sizes to a 4-level scale (30 mins)",
                "5. Do a final accessibility check with Lighthouse or WAVE"
            ]
        }

    async def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """
        Answer follow-up questions about the design audit.
        
        Args:
            question: User's question about the feedback
            context: Previous audit results and feedback
            
        Returns:
            Answer to the question
        """
        system_prompt = f"""You are an expert design mentor answering questions about a design audit.
Context from the audit: {json.dumps(context, indent=2)}

Answer questions directly, helpfully, and with reference to the specific design and feedback."""
        
        try:
            # TODO: Call LLM API
            # response = self.client.chat.completions.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": system_prompt},
            #         {"role": "user", "content": question}
            #     ],
            #     temperature=0.7,
            #     max_tokens=500
            # )
            # return response.choices[0].message.content
            
            return f"To answer your question about {question[:30]}..., consider reviewing the accessibility guidelines linked in the resources section."
            
        except Exception as e:
            raise Exception(f"Question answering failed: {str(e)}")
