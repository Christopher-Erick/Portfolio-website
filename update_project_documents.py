#!/usr/bin/env python
"""
Script to update project documents to use raw file URLs
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
os.chdir(project_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from portfolio.models import Project

def update_project_documents():
    """Update project documents to use raw file URLs"""
    # Raw file URLs we just uploaded
    raw_urls = {
        "christopher_otieno_cs_sa10_25079_malware_introductory.docx": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914078/writeups_raw/Christopher_Otieno_CS-SA10-25079_Malware_introductory.docx.pdf",
        "malware_analysis": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914110/writeups_raw/Malware_Analysis.pdf",
        "metasploit_penetration_cookbook_second_edition_": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914159/writeups_raw/Metasploit_Penetration_Cookbook_Second_Edition_.pdf",
        "security_assesment": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914162/writeups_raw/SECURITY_ASSESSEMENT.pdf",
        "splunk_exploring_spl": "https://res.cloudinary.com/dge5xurfz/raw/upload/v1758914165/writeups_raw/Splunk_Exploring_SPL.pdf"
    }
    
    # Get all projects
    projects = getattr(Project, 'objects').all()
    
    # Mapping of project titles to document keys
    project_document_mapping = {
        "Vulnerability Assessment - Nessus and OpenVAS Implementation": "security_assesment",
        "SIEM Log Analysis with Splunk SPL - Advanced Query Techniques": "splunk_exploring_spl",
        "Malware Analysis Fundamentals - Static and Dynamic Analysis Techniques": "malware_analysis"
    }
    
    print("Updating project documents...")
    print("=" * 50)
    
    for project in projects:
        print(f"\nProcessing project: {project.title}")
        
        # Check if this project needs a document update
        if project.title in project_document_mapping:
            doc_key = project_document_mapping[project.title]
            if doc_key in raw_urls:
                new_url = raw_urls[doc_key]
                old_url = str(project.writeup_document) if project.writeup_document else "None"
                
                print(f"  Updating document: {old_url} -> {new_url}")
                project.writeup_document.name = new_url
                project.save(update_fields=['writeup_document'])
                print(f"  ✓ Document updated successfully")
            else:
                print(f"  ? No raw URL found for document key: {doc_key}")
        else:
            print(f"  ? No document mapping found for this project")
    
    print("\nDocument update process completed!")

if __name__ == '__main__':
    update_project_documents()