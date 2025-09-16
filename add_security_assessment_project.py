#!/usr/bin/env python
"""
Add Security Assessment Methodology Study Project to Portfolio
"""
import os
import sys
import django
from datetime import date

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from portfolio.models import Category, Technology, Project, ProjectFeature


def create_security_assessment_project():
    """Create the Security Assessment Methodology project"""
    
    # Get the appropriate category
    try:
        assessment_cat = Category.objects.get(slug='security-assessment')
    except Category.DoesNotExist:
        print("Security Assessment category not found")
        return
    
    project_data = {
        'title': 'Comprehensive Security Assessment Methodology Study',
        'slug': 'security-assessment-methodology-study',
        'short_description': 'In-depth study and analysis of security assessment methodologies including vulnerability assessments, penetration testing, red team operations, and compliance frameworks.',
        'description': '''Completed comprehensive study of security assessment methodologies and frameworks essential for cybersecurity operations. This foundational project demonstrates understanding of various security testing approaches and their appropriate applications in different organizational contexts.

## Study Overview

This intensive 2-week study covered multiple security assessment methodologies, providing a solid foundation for practical cybersecurity operations:

### Key Learning Areas:

**1. Vulnerability Assessment Frameworks**
• Understanding compliance-based security standards (GDPR, PCI-DSS, OWASP)
• Systematic vulnerability identification and validation processes
• Risk assessment and prioritization methodologies
• Vulnerability scanning tools and manual verification techniques

**2. Penetration Testing Methodologies**
• Black box testing: External attacker perspective with minimal knowledge
• Grey box testing: Internal user perspective with limited system knowledge
• White box testing: Full access assessment with complete system documentation
• Specialized testing areas: Application, network, physical, and social engineering

**3. Advanced Security Assessment Types**
• Red Team Assessments: Evasive, goal-oriented attack simulations
• Purple Team Operations: Collaborative offensive-defensive security exercises
• Bug Bounty Programs: Crowdsourced vulnerability discovery
• Security Audits: Compliance-driven external assessments

**4. Organizational Security Maturity**
• Assessment of security program maturity levels
• Appropriate testing methods for different maturity stages
• Building security culture and awareness programs
• Integration of security assessments into organizational processes

## Practical Applications Studied:

**Assessment Selection Criteria:**
• Matching assessment types to organizational security maturity
• Cost-benefit analysis of different testing approaches
• Compliance requirements and regulatory considerations
• Resource allocation and expertise requirements

**Industry-Specific Applications:**
• Payment Card Industry (PCI-DSS) compliance assessments
• Healthcare (HIPAA) security evaluations
• Financial services regulatory requirements
• Government and critical infrastructure protections

**Tool and Technique Analysis:**
• Vulnerability scanners vs. manual testing approaches
• Automated vs. manual penetration testing techniques
• Social engineering and physical security assessment methods
• Continuous monitoring and assessment integration

## Key Insights Gained:

**Strategic Understanding:**
• Different assessment types serve distinct purposes in security programs
• Vulnerability assessments provide broad coverage, pentests provide depth
• Security maturity determines appropriate assessment frequency and type
• Integration of multiple assessment types creates comprehensive security programs

**Operational Knowledge:**
• Legal and ethical considerations in security testing
• Proper scoping and authorization requirements
• Report writing and communication of findings
• Remediation prioritization and tracking methodologies

**Technical Foundations:**
• Understanding of common vulnerability classes and exploitation techniques
• Network security assessment approaches and methodologies
• Web application security testing frameworks (OWASP Top 10)
• Infrastructure and system security evaluation methods

This foundational study provides the theoretical framework necessary for conducting effective security assessments and understanding their role in comprehensive cybersecurity programs. The knowledge gained directly supports practical application in vulnerability assessments, penetration testing, and security program development.''',
        'category': assessment_cat,
        'status': 'completed',
        'start_date': date(2024, 7, 1),
        'end_date': date(2024, 7, 14),
        'is_featured': True
    }
    
    # Create the project
    project, created = Project.objects.get_or_create(
        slug=project_data['slug'],
        defaults=project_data
    )
    
    if created:
        print(f"Created project: {project.title}")
        
        # Add relevant technologies
        tech_names = [
            'OWASP', 'NIST', 'ISO 27001', 'Nessus', 'Nmap', 
            'Burp Suite', 'Metasploit', 'Kali Linux'
        ]
        
        for tech_name in tech_names:
            try:
                tech = Technology.objects.get(name=tech_name)
                project.technologies.add(tech)
            except Technology.DoesNotExist:
                print(f"Technology '{tech_name}' not found")
        
        project.save()
        
        # Create project features
        features = [
            {
                'title': 'Vulnerability Assessment Framework',
                'description': 'Comprehensive understanding of vulnerability assessment methodologies, compliance standards, and systematic vulnerability identification processes.',
                'icon': 'fas fa-search',
                'order': 1
            },
            {
                'title': 'Penetration Testing Methodologies',
                'description': 'In-depth knowledge of black box, grey box, and white box testing approaches with specialized focus areas including application and network testing.',
                'icon': 'fas fa-bug',
                'order': 2
            },
            {
                'title': 'Security Maturity Assessment',
                'description': 'Understanding of organizational security maturity levels and appropriate assessment selection based on organizational readiness and capabilities.',
                'icon': 'fas fa-chart-line',
                'order': 3
            },
            {
                'title': 'Advanced Assessment Types',
                'description': 'Knowledge of red team, purple team, bug bounty, and security audit methodologies with understanding of their specific applications and benefits.',
                'icon': 'fas fa-shield-alt',
                'order': 4
            }
        ]
        
        for feature_data in features:
            feature_data['project'] = project
            ProjectFeature.objects.get_or_create(
                project=project,
                title=feature_data['title'],
                defaults=feature_data
            )
        
        print(f"Added {len(features)} features to the project")
    else:
        print(f"Project already exists: {project.title}")


def main():
    print("Adding Security Assessment Methodology Study project...")
    create_security_assessment_project()
    print("Project creation completed!")


if __name__ == '__main__':
    main()