"""Tests for skills extraction functionality."""

import pytest

from app.core.analysis.skills_extractor import SkillsExtractor
from app.core.analysis.skill_database import SkillDatabase, SkillCategory


class TestSkillDatabase:
    """Test the skills database functionality."""
    
    def test_skill_database_initialization(self):
        """Test that skill database initializes correctly."""
        db = SkillDatabase()
        assert db is not None
        assert len(db._skill_data) > 0

    def test_canonical_skill_names(self):
        """Test that canonical skill names are properly defined."""
        db = SkillDatabase()
        
        # Check some common skills exist
        programming_skills = db._skill_data[SkillCategory.PROGRAMMING_LANGUAGES]
        assert "Python" in programming_skills
        assert "JavaScript" in programming_skills
        assert "SQL" in programming_skills

    def test_skill_categories(self):
        """Test skill categorization."""
        db = SkillDatabase()
        
        # Check categories exist
        assert SkillCategory.PROGRAMMING_LANGUAGES in db._skill_data
        assert SkillCategory.FRAMEWORKS in db._skill_data
        assert SkillCategory.DATABASES in db._skill_data

    def test_skill_search(self):
        """Test skill search functionality."""
        db = SkillDatabase()
        
        # Test finding skills by variations
        programming_skills = db._skill_data[SkillCategory.PROGRAMMING_LANGUAGES]
        assert "python" in programming_skills["Python"]  # lowercase variation


class TestSkillsExtractor:
    """Test the skills extractor functionality."""

    def test_extract_skills_from_simple_text(self):
        """Test extracting skills from simple CV text."""
        extractor = SkillsExtractor()
        
        cv_text = """
        Software Developer
        
        Skills: Python, JavaScript, React, PostgreSQL
        Experience with Django and Flask frameworks.
        """
        
        result = extractor.extract_skills(cv_text)
        
        assert result is not None
        assert "Python" in result.all_skills
        assert "JavaScript" in result.all_skills
        assert "React" in result.all_skills
        assert "PostgreSQL" in result.all_skills
        assert result.total_skills_found >= 4

    def test_extract_skills_with_experience(self):
        """Test that we can extract skills even when mentioned with experience."""
        extractor = SkillsExtractor()
        
        cv_text = """
        Software Developer with 8 years experience in Python and 3 years in React.
        Expertise in machine learning and data analysis.
        """
        
        result = extractor.extract_skills(cv_text)
        
        # Should find skills regardless of experience context
        assert "Python" in result.all_skills
        assert "React" in result.all_skills
        assert result.total_skills_found > 0

    def test_extract_skills_from_skills_section(self):
        """Test extracting from a typical skills section."""
        extractor = SkillsExtractor()
        
        cv_text = """
        TECHNICAL SKILLS
        - Programming: Python, JavaScript, Java
        - Web: React, Django, Flask
        - Databases: MySQL, PostgreSQL
        - Cloud: AWS, Docker
        """
        
        result = extractor.extract_skills(cv_text)
        
        expected_skills = ["Python", "JavaScript", "Java", "React", "Django", "Flask", "MySQL", "PostgreSQL"]
        
        for skill in expected_skills:
            assert skill in result.all_skills, f"Expected skill '{skill}' not found"
        
        assert result.total_skills_found >= len(expected_skills)

    def test_skills_categorization(self):
        """Test that skills are properly categorized."""
        extractor = SkillsExtractor()
        
        cv_text = """
        Technical Skills:
        - Languages: Python, Java
        - Databases: MySQL, MongoDB
        - Frameworks: React, Django
        """
        
        result = extractor.extract_skills(cv_text)
        
        # Check categorization
        assert "Programming Languages" in result.skills_by_category
        assert "Databases" in result.skills_by_category
        assert "Frameworks" in result.skills_by_category

    def test_basic_skill_detection(self):
        """Test that we can detect skills in various contexts."""
        extractor = SkillsExtractor()
        
        # High confidence text with experience
        cv_text = """
        Senior Python Developer with 10 years of experience.
        Expert in Django framework and PostgreSQL database administration.
        """
        
        result = extractor.extract_skills(cv_text)
        
        # Should find these skills
        assert "Python" in result.all_skills
        assert "Django" in result.all_skills
        assert "PostgreSQL" in result.all_skills
        assert result.total_skills_found >= 3

    def test_empty_text_handling(self):
        """Test handling of empty or invalid text."""
        extractor = SkillsExtractor()
        
        # Empty text
        result = extractor.extract_skills("")
        assert result.total_skills_found == 0
        assert len(result.all_skills) == 0

    def test_basic_functionality(self):
        """Test basic skills extraction functionality."""
        extractor = SkillsExtractor()
        
        cv_text = """
        Data Scientist with Python experience.
        Worked with machine learning and statistical analysis.
        Experience with SQL databases and data visualization.
        """
        
        result = extractor.extract_skills(cv_text)
        
        # Basic assertions
        assert isinstance(result.all_skills, list)
        assert isinstance(result.skills_by_category, dict)
        assert isinstance(result.total_skills_found, int)
        assert result.total_skills_found >= 0