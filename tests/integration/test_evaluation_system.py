"""Integration test for the complete CV evaluation workflow."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_complete_cv_evaluation_workflow():
    """Test the complete workflow: upload CV, then evaluate it."""
    
    # Step 1: Upload a CV
    cv_content = """
    John Doe
    Senior Data Scientist
    john.doe@example.com | +1-555-123-4567
    
    EXPERIENCE:
    Senior Data Scientist at TechCorp (2020-Present)
    - Led machine learning initiatives improving model accuracy by 25%
    - Managed team of 5 data scientists and engineers
    - Deployed 10+ production ML models using Python, TensorFlow, AWS
    - Built end-to-end data pipelines processing 1TB+ daily data
    
    Data Scientist at StartupXYZ (2018-2020)  
    - Developed predictive models using scikit-learn, pandas, SQL
    - Created interactive dashboards with Tableau and D3.js
    - Collaborated with product team on A/B testing framework
    
    EDUCATION:
    Master of Science in Computer Science, Stanford University (2018)
    - Thesis: Deep Learning for Natural Language Processing
    - GPA: 3.8/4.0
    
    Bachelor of Science in Mathematics, UC Berkeley (2016)
    - Magna Cum Laude, Dean's List
    
    SKILLS:
    Programming: Python, R, SQL, Java, JavaScript
    Machine Learning: TensorFlow, PyTorch, scikit-learn, XGBoost
    Data Tools: Pandas, NumPy, Matplotlib, Seaborn, Jupyter
    Cloud: AWS (EC2, S3, SageMaker), Docker, Kubernetes
    Databases: PostgreSQL, MongoDB, Redis
    Visualization: Tableau, Power BI, D3.js, Plotly
    
    CERTIFICATIONS:
    - AWS Certified Machine Learning Specialty (2021)
    - Google Cloud Professional Data Engineer (2020)
    """
    
    # Upload the CV
    files = {"file": ("test_cv.txt", cv_content, "text/plain")}
    upload_response = client.post("/api/v1/upload", files=files)
    
    assert upload_response.status_code == 201  # Upload returns 201 Created
    upload_data = upload_response.json()
    upload_id = upload_data["upload_id"]
    
    
    # Step 2: Perform General Market Evaluation
    eval_response = client.get(f"/api/v1/evaluate/general/{upload_id}")
    
    assert eval_response.status_code == 200
    
    eval_data = eval_response.json()
    
    
    # Verify evaluation structure
    assert "evaluation_id" in eval_data
    assert "skills_score" in eval_data
    assert "experience_score" in eval_data  
    assert "education_score" in eval_data
    assert "strengths" in eval_data
    assert "improvement_areas" in eval_data
    assert "recommendations" in eval_data
    
    # Step 3: Test Comprehensive Evaluation
    comp_response = client.post(f"/api/v1/evaluate/comprehensive/{upload_id}")
    assert comp_response.status_code == 200
    
    comp_data = comp_response.json()
    assert "general_evaluation" in comp_data
    assert "additional_insights" in comp_data
    
    
    # Step 4: Retrieve Results by ID
    evaluation_id = eval_data["evaluation_id"]
    result_response = client.get(f"/api/v1/results/{evaluation_id}")
    assert result_response.status_code == 200
    
    result_data = result_response.json()
    assert result_data["evaluation_id"] == evaluation_id
    assert result_data["total_score"] == eval_data["total_score"]
    
    
    # Step 5: List All Results
    all_results_response = client.get("/api/v1/results/")
    assert all_results_response.status_code == 200
    
    all_results = all_results_response.json()
    assert all_results["total_count"] >= 1
    assert evaluation_id in all_results["evaluations"]
    
    
    # Print detailed breakdown
    skills = eval_data["skills_score"]
    experience = eval_data["experience_score"] 
    education = eval_data["education_score"]
    
    
    
    
    
    # Verify this is a strong profile
    assert eval_data["total_score"] >= 70, "This should be a strong profile"
    assert eval_data["score_level"] in ["Good", "Excellent"], "Should be good or excellent"
    assert len(skills.get("high_demand_skills", [])) >= 5, "Should have many high-demand skills"
    
    return {
        "upload_id": upload_id,
        "evaluation_id": evaluation_id, 
        "total_score": eval_data["total_score"],
        "score_level": eval_data["score_level"]
    }


def test_evaluation_with_basic_cv():
    """Test evaluation with a more basic CV profile."""
    
    basic_cv = """
    Jane Smith
    Data Analyst
    jane@email.com
    
    EXPERIENCE:
    Data Analyst at SmallCorp (2022-Present)
    - Created reports using Excel and SQL
    - Analyzed customer data for insights
    
    EDUCATION:
    Bachelor in Business Administration (2022)
    
    SKILLS:
    Excel, SQL, Python basics, Tableau
    """
    
    # Upload basic CV
    files = {"file": ("basic_cv.txt", basic_cv, "text/plain")}
    upload_response = client.post("/api/v1/upload", files=files)
    assert upload_response.status_code == 201  # Upload returns 201 Created
    
    upload_id = upload_response.json()["upload_id"]
    
    # Evaluate
    eval_response = client.get(f"/api/v1/evaluate/general/{upload_id}")
    assert eval_response.status_code == 200
    
    eval_data = eval_response.json()
    
    
    # This should be a lower score
    assert eval_data["total_score"] < 70, "Basic CV should have lower score"
    assert eval_data["score_level"] in ["Fair", "Needs Improvement"], "Should need improvement"
    
    return eval_data


if __name__ == "__main__":
    # Run the tests directly
    
    result1 = test_complete_cv_evaluation_workflow()
    
    result2 = test_evaluation_with_basic_cv()  
    
