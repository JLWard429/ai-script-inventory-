"""Test module for forensic medical investigation infrastructure."""

import pytest
from pathlib import Path


class TestForensicInfrastructure:
    """Tests for the forensic-grade medical investigation infrastructure."""

    def test_private_care_directory_exists(self):
        """Test that the private/care directory exists."""
        care_dir = Path("private/care")
        assert care_dir.exists()
        assert care_dir.is_dir()

    def test_required_infrastructure_files_exist(self):
        """Test that all required infrastructure files exist."""
        required_files = [
            "_STAGING_README.txt",
            "MASTER_DOCUMENT_INDEX.md",
            "KNOWLEDGE_AND_LEARNING_LOG.md",
            "FORENSIC_ERROR_LOG.md",
            "TASK_PROGRESS_LOG_TEMPLATE.md",
            "FILE_FOLDER_MANAGEMENT_GUIDE.md",
            "AUTOMATED_REVIEW_SCAN_GUIDE.md",
        ]
        
        care_dir = Path("private/care")
        for filename in required_files:
            file_path = care_dir / filename
            assert file_path.exists(), f"Required file {filename} does not exist"
            assert file_path.is_file(), f"{filename} is not a regular file"

    def test_staging_readme_content_quality(self):
        """Test that the staging README contains essential sections."""
        staging_readme = Path("private/care/_STAGING_README.txt")
        content = staging_readme.read_text()
        
        # Check for key sections
        assert "STAGING WORKFLOW" in content
        assert "QUALITY CONTROL REQUIREMENTS" in content
        assert "TRIAGE CHECKLIST" in content
        assert "ESCALATION PROCEDURES" in content
        assert "REVISION HISTORY" in content

    def test_master_document_index_structure(self):
        """Test that the master document index has proper structure."""
        master_index = Path("private/care/MASTER_DOCUMENT_INDEX.md")
        content = master_index.read_text()
        
        # Check for key sections
        assert "# Master Document Index" in content
        assert "## Document Categories" in content
        assert "## Document Registry" in content
        assert "## Active Documents" in content
        assert "## Search and Retrieval" in content

    def test_knowledge_log_framework(self):
        """Test that the knowledge and learning log has proper framework."""
        knowledge_log = Path("private/care/KNOWLEDGE_AND_LEARNING_LOG.md")
        content = knowledge_log.read_text()
        
        # Check for key sections
        assert "# Knowledge and Learning Log" in content
        assert "## Regulatory Framework Tracking" in content
        assert "## Learning Entries" in content
        assert "## Training and Certification Tracking" in content
        assert "## Continuous Improvement Process" in content

    def test_error_log_classification_system(self):
        """Test that the forensic error log has proper classification."""
        error_log = Path("private/care/FORENSIC_ERROR_LOG.md")
        content = error_log.read_text()
        
        # Check for key sections
        assert "# Forensic Error Log" in content
        assert "## Error Classification System" in content
        assert "### Severity Levels" in content
        assert "CRITICAL" in content
        assert "HIGH" in content
        assert "MEDIUM" in content
        assert "LOW" in content

    def test_task_progress_template_completeness(self):
        """Test that the task progress template is comprehensive."""
        task_template = Path("private/care/TASK_PROGRESS_LOG_TEMPLATE.md")
        content = task_template.read_text()
        
        # Check for key sections
        assert "# Task Progress Log Template" in content
        assert "## Case Information" in content
        assert "## Evidence Management" in content
        assert "## Quality Assurance" in content
        assert "## Conclusions and Recommendations" in content
        assert "## Signatures and Approvals" in content

    def test_file_management_guide_procedures(self):
        """Test that the file management guide has proper procedures."""
        file_guide = Path("private/care/FILE_FOLDER_MANAGEMENT_GUIDE.md")
        content = file_guide.read_text()
        
        # Check for key sections
        assert "# File and Folder Management Guide" in content
        assert "## File Operation Procedures" in content
        assert "### File Creation Protocol" in content
        assert "### File Movement Protocol" in content
        assert "### File Deletion Protocol" in content

    def test_automated_review_guide_workflow(self):
        """Test that the automated review guide has proper workflow."""
        review_guide = Path("private/care/AUTOMATED_REVIEW_SCAN_GUIDE.md")
        content = review_guide.read_text()
        
        # Check for key sections
        assert "# Automated Review Scan Guide" in content
        assert "## Automated Review Framework" in content
        assert "## Error Detection Protocols" in content
        assert "## Compliance Verification Workflow" in content
        assert "## Cross-Reference Analysis" in content

    def test_file_sizes_reasonable(self):
        """Test that all files have reasonable content size."""
        care_dir = Path("private/care")
        for file_path in care_dir.iterdir():
            if file_path.is_file():
                size = file_path.stat().st_size
                # Each file should be at least 1KB (substantial content)
                assert size > 1000, f"File {file_path.name} seems too small: {size} bytes"
                # But not unreasonably large (over 100KB would be excessive for docs)
                assert size < 100000, f"File {file_path.name} seems too large: {size} bytes"

    def test_markdown_formatting_compliance(self):
        """Test that markdown files follow proper formatting."""
        care_dir = Path("private/care")
        md_files = care_dir.glob("*.md")
        
        for md_file in md_files:
            content = md_file.read_text()
            
            # Should start with a proper heading
            assert content.startswith("#"), f"File {md_file.name} should start with a heading"
            
            # Should contain proper metadata sections
            lines = content.split('\n')
            header_lines = lines[:10]  # Check first 10 lines for metadata
            header_text = '\n'.join(header_lines)
            
            # Should have version info
            assert ("Version:" in header_text or 
                   "Template Version:" in header_text), f"File {md_file.name} missing version info"

    def test_forensic_grade_requirements(self):
        """Test that files meet forensic-grade documentation requirements."""
        care_dir = Path("private/care")
        
        for file_path in care_dir.iterdir():
            if file_path.is_file():
                content = file_path.read_text()
                
                # Should mention audit trails or tracking
                assert any(keyword in content.lower() for keyword in 
                          ["audit trail", "traceability", "chain of custody", "verification"]), \
                          f"File {file_path.name} lacks forensic-grade audit requirements"
                
                # Should have version control or tracking
                assert any(keyword in content.lower() for keyword in 
                          ["version", "date", "approval", "review"]), \
                          f"File {file_path.name} lacks proper version control"

    def test_medical_legal_focus(self):
        """Test that files are properly focused on medical/legal investigations."""
        care_dir = Path("private/care")
        
        for file_path in care_dir.iterdir():
            if file_path.is_file():
                content = file_path.read_text()
                
                # Should reference medical or legal context
                assert any(keyword in content.lower() for keyword in 
                          ["medical", "legal", "regulatory", "compliance", "investigation"]), \
                          f"File {file_path.name} lacks medical/legal context"