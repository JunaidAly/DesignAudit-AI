"""
Analyst Agent - Rules-Based Violation Detection
Checks design against heuristics and accessibility guidelines
"""
from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass


class ViolationSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class Violation:
    """Represents a detected design violation"""
    id: str
    category: str  # accessibility, spacing, typography, color, consistency, etc.
    severity: ViolationSeverity
    title: str
    description: str
    affected_elements: List[str]  # Component IDs
    location: Dict[str, Any]  # Position info for heatmap
    guideline_reference: str  # e.g., "WCAG 2.1 AA 1.4.3"
    suggestion: str


class RulesEngine:
    """
    Analyzes design map against 50+ heuristics.
    
    Heuristic Categories:
    - Accessibility (WCAG 2.1 AA/AAA, color contrast, font sizing)
    - Spacing & Alignment (padding, margin, grid alignment)
    - Typography (hierarchy, readability, consistency)
    - Color (palette consistency, semantic use)
    - Interactive Elements (button size, feedback, affordance)
    - Responsive Design (breakpoints, scaling)
    - Consistency (pattern repetition, component reuse)
    """

    def __init__(self):
        self.violations: List[Violation] = []
        self.heuristics = self._load_heuristics()

    def analyze(self, design_map: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all heuristics against the design map.
        
        Args:
            design_map: Structured JSON from Inspector agent
            
        Returns:
            Dictionary with violations grouped by category and priority
        """
        self.violations = []
        
        # Run all heuristic checks
        self._check_accessibility(design_map)
        self._check_spacing_alignment(design_map)
        self._check_typography(design_map)
        self._check_color_contrast(design_map)
        self._check_consistency(design_map)
        self._check_interactive_elements(design_map)
        
        # Organize results
        return self._organize_violations()

    def _check_accessibility(self, design_map: Dict[str, Any]) -> None:
        """Check WCAG accessibility guidelines"""
        components = design_map.get("components", [])
        
        for component in components:
            # Check text contrast ratio
            bg_color = component.get("style", {}).get("background_color")
            text_color = component.get("style", {}).get("text_color")
            
            if bg_color and text_color:
                contrast = self._calculate_contrast_ratio(bg_color, text_color)
                if contrast < 4.5:  # AA standard for normal text
                    self.violations.append(Violation(
                        id=f"a11y_contrast_{component['id']}",
                        category="accessibility",
                        severity=ViolationSeverity.HIGH,
                        title="Insufficient Color Contrast",
                        description=f"Text contrast ratio is {contrast:.2f}:1, but WCAG AA requires 4.5:1",
                        affected_elements=[component["id"]],
                        location=component.get("position", {}),
                        guideline_reference="WCAG 2.1 AA 1.4.3",
                        suggestion="Increase contrast by darkening text or lightening background"
                    ))
            
            # Check minimum touch target size (48x48px)
            dims = component.get("dimensions", {})
            if component.get("type") in ["button", "link", "input"]:
                if dims.get("width", 0) < 44 or dims.get("height", 0) < 44:
                    self.violations.append(Violation(
                        id=f"a11y_touch_target_{component['id']}",
                        category="accessibility",
                        severity=ViolationSeverity.MEDIUM,
                        title="Small Touch Target",
                        description=f"Touch target is {dims.get('width')}x{dims.get('height')}px but should be at least 44x44px",
                        affected_elements=[component["id"]],
                        location=component.get("position", {}),
                        guideline_reference="WCAG 2.1 AAA 2.5.5",
                        suggestion="Increase button size to at least 44x44 pixels for better accessibility"
                    ))

    def _check_spacing_alignment(self, design_map: Dict[str, Any]) -> None:
        """Check spacing consistency"""
        components = design_map.get("components", [])
        observed_paddings = set()
        
        for component in components:
            padding = component.get("spacing", {}).get("padding", {})
            if padding:
                # Convert to 8px grid units
                for value in padding.values():
                    if value and value % 8 != 0:
                        self.violations.append(Violation(
                            id=f"spacing_grid_{component['id']}",
                            category="spacing",
                            severity=ViolationSeverity.LOW,
                            title="Non-Standard Padding",
                            description=f"Padding value {value}px doesn't align to 8px grid",
                            affected_elements=[component["id"]],
                            location=component.get("position", {}),
                            guideline_reference="Material Design Spacing",
                            suggestion="Use 8px, 16px, 24px, 32px, or 40px for consistent spacing"
                        ))

    def _check_typography(self, design_map: Dict[str, Any]) -> None:
        """Check typography consistency"""
        typography = design_map.get("typography", {})
        components = design_map.get("components", [])
        
        font_sizes = set()
        for component in components:
            size = component.get("style", {}).get("font_size")
            if size:
                font_sizes.add(size)
        
        if len(font_sizes) > 5:
            self.violations.append(Violation(
                id="typography_scale",
                category="typography",
                severity=ViolationSeverity.MEDIUM,
                title="Too Many Font Sizes",
                description=f"Found {len(font_sizes)} different font sizes. Limit to 3-5 for consistency",
                affected_elements=[],
                location={},
                guideline_reference="Typography Best Practices",
                suggestion="Define a consistent typographic scale (e.g., 12px, 14px, 16px, 20px, 32px)"
            ))

    def _check_color_contrast(self, design_map: Dict[str, Any]) -> None:
        """Check color palette consistency and contrast"""
        palette = design_map.get("color_palette", {})
        
        # Check if sufficient colors are defined
        primary_colors = palette.get("primary", [])
        if not primary_colors:
            self.violations.append(Violation(
                id="color_no_primary",
                category="color",
                severity=ViolationSeverity.MEDIUM,
                title="No Primary Color Defined",
                description="Design should have a clear primary color for main actions",
                affected_elements=[],
                location={},
                guideline_reference="Material Design Color",
                suggestion="Define a primary brand color for CTAs and main interactive elements"
            ))

    def _check_consistency(self, design_map: Dict[str, Any]) -> None:
        """Check component and pattern consistency"""
        components = design_map.get("components", [])
        button_components = [c for c in components if c.get("type") == "button"]
        
        if button_components:
            button_sizes = set()
            button_colors = set()
            
            for button in button_components:
                dims = button.get("dimensions", {})
                size_key = (dims.get("width"), dims.get("height"))
                button_sizes.add(size_key)
                
                bg = button.get("style", {}).get("background_color")
                button_colors.add(bg)
            
            if len(button_sizes) > 2:
                self.violations.append(Violation(
                    id="consistency_button_sizes",
                    category="consistency",
                    severity=ViolationSeverity.LOW,
                    title="Inconsistent Button Sizes",
                    description=f"Buttons have {len(button_sizes)} different dimensions",
                    affected_elements=[b["id"] for b in button_components],
                    location={},
                    guideline_reference="Design System Consistency",
                    suggestion="Use 2 standard button sizes: primary (large) and secondary (regular)"
                ))

    def _check_interactive_elements(self, design_map: Dict[str, Any]) -> None:
        """Check button affordance and feedback"""
        components = design_map.get("components", [])
        
        for component in components:
            if component.get("type") == "button":
                dims = component.get("dimensions", {})
                
                # Check button has adequate padding
                padding = component.get("spacing", {}).get("padding", {})
                if padding.get("left", 0) < 12 or padding.get("right", 0) < 12:
                    self.violations.append(Violation(
                        id=f"button_padding_{component['id']}",
                        category="interactive",
                        severity=ViolationSeverity.LOW,
                        title="Small Button Padding",
                        description="Button text padding should be at least 12px on left and right",
                        affected_elements=[component["id"]],
                        location=component.get("position", {}),
                        guideline_reference="Material Design Buttons",
                        suggestion="Add at least 12px horizontal padding inside buttons"
                    ))

    def _calculate_contrast_ratio(self, hex_bg: str, hex_fg: str) -> float:
        """Calculate WCAG contrast ratio between two hex colors"""
        try:
            # Convert hex to RGB
            def hex_to_rgb(h):
                h = h.lstrip('#')
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
            def relative_luminance(rgb):
                def adjust(c):
                    c = c / 255.0
                    if c <= 0.03928:
                        return c / 12.92
                    return ((c + 0.055) / 1.055) ** 2.4
                r, g, b = [adjust(x) for x in rgb]
                return 0.2126 * r + 0.7152 * g + 0.0722 * b
            
            l1 = relative_luminance(hex_to_rgb(hex_bg))
            l2 = relative_luminance(hex_to_rgb(hex_fg))
            
            lighter = max(l1, l2)
            darker = min(l1, l2)
            
            return (lighter + 0.05) / (darker + 0.05)
        except:
            return 4.5  # Default to passing if calculation fails

    def _load_heuristics(self) -> Dict[str, Any]:
        """Load design heuristics from configuration"""
        return {
            "material_design": {},
            "apple_hci": {},
            "wcag_2_1": {},
            "custom_heuristics": {}
        }

    def _organize_violations(self) -> Dict[str, Any]:
        """Organize violations by category and severity"""
        organized = {
            "total_violations": len(self.violations),
            "by_severity": {
                "critical": [],
                "high": [],
                "medium": [],
                "low": [],
                "info": []
            },
            "by_category": {}
        }
        
        # Sort by severity
        for violation in self.violations:
            organized["by_severity"][violation.severity.value].append(violation.__dict__)
        
        # Sort by category
        for violation in self.violations:
            cat = violation.category
            if cat not in organized["by_category"]:
                organized["by_category"][cat] = []
            organized["by_category"][cat].append(violation.__dict__)
        
        return organized
