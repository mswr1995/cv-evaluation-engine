"""Simple skills extraction service."""

import logging
import re
from typing import Dict, List, Optional
from dataclasses import dataclass

from app.core.analysis.skill_database import SkillCategory, SkillDatabase

logger = logging.getLogger(__name__)


@dataclass
class ExtractedSkills:
    """Container for extracted skills with metadata."""
    technical_skills: List[str]
    soft_skills: List[str]
    all_skills: List[str]
    skills_by_category: Dict[str, List[str]]
    total_skills_found: int = 0


class SkillsExtractor:
    """Simple keyword-based skills extraction service."""
    
    def __init__(self):
        """Initialize the skills extractor with skill database."""
        self.skill_db = SkillDatabase()
        logger.info("SkillsExtractor initialized with simple keyword matching")
    
    def extract_skills(self, text: str) -> ExtractedSkills:
        """
        Extract skills from CV text using keyword matching.
        
        Args:
            text: CV text content
            
        Returns:
            ExtractedSkills: Container with found skills organized by category
        """
        if not text:
            return self._empty_result()
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        found_skills = []
        skills_by_category = {}
        
        # Search for skills in each category
        for category, skills_dict in self.skill_db._skill_data.items():
            category_skills = []
            
            for canonical_skill, variations in skills_dict.items():
                # Check if any variation of this skill appears in text
                for variation in [canonical_skill.lower()] + [v.lower() for v in variations]:
                    if self._skill_found_in_text(variation, text_lower):
                        if canonical_skill not in found_skills:
                            found_skills.append(canonical_skill)
                            category_skills.append(canonical_skill)
                        break
            
            if category_skills:
                skills_by_category[category.value] = category_skills
        
        # Separate technical and soft skills
        technical_skills = []
        soft_skills = []
        
        for skill in found_skills:
            if self._is_technical_skill(skill):
                technical_skills.append(skill)
            else:
                soft_skills.append(skill)
        
        return ExtractedSkills(
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            all_skills=found_skills,
            skills_by_category=skills_by_category,
            total_skills_found=len(found_skills)
        )
    
    def _skill_found_in_text(self, skill: str, text: str) -> bool:
        """Check if a skill is found in text using word boundaries."""
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        return bool(re.search(pattern, text, re.IGNORECASE))
    
    def _is_technical_skill(self, skill: str) -> bool:
        """Determine if a skill is technical based on its category."""
        technical_categories = [
            SkillCategory.PROGRAMMING_LANGUAGES,
            SkillCategory.FRAMEWORKS,
            SkillCategory.DATABASES,
            SkillCategory.CLOUD_PLATFORMS,
            SkillCategory.TOOLS_SOFTWARE,
            SkillCategory.DATA_SCIENCE,
            SkillCategory.WEB_TECHNOLOGIES,
            SkillCategory.MOBILE_DEVELOPMENT,
            SkillCategory.DEVOPS
        ]
        
        for category in technical_categories:
            if skill in self.skill_db._skill_data.get(category, {}):
                return True
        return False
    
    def _empty_result(self) -> ExtractedSkills:
        """Return empty skills result."""
        return ExtractedSkills(
            technical_skills=[],
            soft_skills=[],
            all_skills=[],
            skills_by_category={},
            total_skills_found=0
        )