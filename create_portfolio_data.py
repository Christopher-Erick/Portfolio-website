#!/usr/bin/env python
"""
Script to create sample cybersecurity portfolio data
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


def create_categories():
    """Create cybersecurity project categories"""
    categories = [
        {
            'name': 'Penetration Testing',
            'slug': 'penetration-testing',
            'description': 'Ethical hacking and penetration testing projects',
            'icon': 'fas fa-bug'
        },
        {
            'name': 'Security Assessment',
            'slug': 'security-assessment',
            'description': 'Vulnerability assessments and security audits',
            'icon': 'fas fa-shield-alt'
        },
        {
            'name': 'SIEM & Monitoring',
            'slug': 'siem-monitoring',
            'description': 'Security Information and Event Management implementations',
            'icon': 'fas fa-eye'
        },
        {
            'name': 'Security Automation',
            'slug': 'security-automation',
            'description': 'Automated security tools and scripts',
            'icon': 'fas fa-robot'
        },
        {
            'name': 'Malware Analysis',
            'slug': 'malware-analysis',
            'description': 'Malware analysis and reverse engineering',
            'icon': 'fas fa-virus'
        }
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")


def create_technologies():
    """Create cybersecurity technologies"""
    technologies = [
        {'name': 'Kali Linux', 'icon': 'fab fa-linux', 'color': '#367588'},
        {'name': 'Wireshark', 'icon': 'fas fa-chart-line', 'color': '#1679A7'},
        {'name': 'Nmap', 'icon': 'fas fa-map', 'color': '#4F81BD'},
        {'name': 'Metasploit', 'icon': 'fas fa-bomb', 'color': '#DC3545'},
        {'name': 'Burp Suite', 'icon': 'fas fa-spider', 'color': '#FF6B00'},
        {'name': 'Nessus', 'icon': 'fas fa-search', 'color': '#00A652'},
        {'name': 'Wazuh', 'icon': 'fas fa-eye', 'color': '#3498DB'},
        {'name': 'Splunk', 'icon': 'fas fa-search-plus', 'color': '#FF6600'},
        {'name': 'Gobuster', 'icon': 'fas fa-spider', 'color': '#28A745'},
        {'name': 'Python', 'icon': 'fab fa-python', 'color': '#3776AB'},
        {'name': 'Bash', 'icon': 'fas fa-terminal', 'color': '#4EAA25'},
        {'name': 'PowerShell', 'icon': 'fab fa-microsoft', 'color': '#5391FE'},
        {'name': 'OWASP', 'icon': 'fas fa-shield-alt', 'color': '#000000'},
        {'name': 'NIST', 'icon': 'fas fa-certificate', 'color': '#0066CC'},
        {'name': 'ISO 27001', 'icon': 'fas fa-certificate', 'color': '#FF9500'}
    ]
    
    for tech_data in technologies:
        technology, created = Technology.objects.get_or_create(
            name=tech_data['name'],
            defaults=tech_data
        )
        if created:
            print(f"Created technology: {technology.name}")


def create_projects():
    """Create sample cybersecurity projects"""
    
    # Get categories and technologies
    pentest_cat = Category.objects.get(slug='penetration-testing')
    assessment_cat = Category.objects.get(slug='security-assessment')
    siem_cat = Category.objects.get(slug='siem-monitoring')
    automation_cat = Category.objects.get(slug='security-automation')
    malware_cat = Category.objects.get(slug='malware-analysis')
    
    projects = [
        {
            'title': 'Enterprise Network Penetration Testing',
            'slug': 'enterprise-network-pentest',
            'short_description': 'Comprehensive penetration test of enterprise network infrastructure identifying critical vulnerabilities and providing detailed remediation guidance.',
            'description': '''Conducted a thorough penetration testing engagement on a medium-sized enterprise network environment. The assessment covered external perimeter testing, internal network segmentation analysis, and privilege escalation scenarios.

Key Activities:
• External reconnaissance and vulnerability scanning using Nmap and Nessus
• Web application security testing with Burp Suite and OWASP methodologies
• Network service enumeration and exploitation using Metasploit framework
• Wireless security assessment including WPA/WPA2 testing
• Social engineering simulation and phishing campaign analysis
• Post-exploitation activities and lateral movement techniques

Results:
• Identified 15 critical and 23 high-severity vulnerabilities
• Successfully gained domain administrator privileges through privilege escalation
• Documented complete attack path from external access to internal compromise
• Provided prioritized remediation roadmap with timeline and resource requirements

This project demonstrated practical application of ethical hacking techniques while maintaining strict adherence to scope and authorization boundaries.''',
            'category': pentest_cat,
            'status': 'completed',
            'start_date': date(2024, 1, 15),
            'end_date': date(2024, 2, 28),
            'github_url': 'https://github.com/Christopher-Erick/network-pentest-toolkit',
            'technologies': ['Kali Linux', 'Nmap', 'Metasploit', 'Burp Suite', 'Wireshark'],
            'is_featured': True
        },
        {
            'title': 'Wazuh SIEM Implementation & Configuration',
            'slug': 'wazuh-siem-implementation',
            'short_description': 'End-to-end deployment of Wazuh SIEM platform with custom rules, dashboards, and automated threat detection capabilities.',
            'description': '''Designed and implemented a comprehensive Security Information and Event Management (SIEM) solution using Wazuh for real-time security monitoring and incident response.

Implementation Details:
• Deployed Wazuh manager and indexer on Ubuntu 20.04 LTS
• Configured agents across Windows and Linux endpoints
• Developed custom detection rules for advanced persistent threats
• Created automated response playbooks for common security incidents
• Integrated with threat intelligence feeds for enhanced detection
• Implemented log analysis for web servers, databases, and network devices

Key Features:
• Real-time monitoring of 50+ endpoints
• Custom dashboards for security operations center (SOC)
• Automated alerting for suspicious activities
• Compliance reporting for ISO 27001 and NIST frameworks
• Integration with external security tools and APIs

The implementation resulted in 40% faster incident response times and significantly improved threat visibility across the organization's infrastructure.''',
            'category': siem_cat,
            'status': 'completed',
            'start_date': date(2024, 3, 1),
            'end_date': date(2024, 4, 15),
            'github_url': 'https://github.com/Christopher-Erick/wazuh-custom-rules',
            'technologies': ['Wazuh', 'Python', 'Bash', 'NIST', 'ISO 27001'],
            'is_featured': True
        },
        {
            'title': 'Web Application Security Assessment',
            'slug': 'web-app-security-assessment',
            'short_description': 'Comprehensive security assessment of web applications using OWASP methodology and automated scanning tools.',
            'description': '''Performed detailed security assessment of multiple web applications following OWASP Top 10 guidelines and industry best practices.

Assessment Scope:
• Static and dynamic application security testing (SAST/DAST)
• Manual penetration testing of authentication mechanisms
• SQL injection and cross-site scripting vulnerability analysis
• Business logic flaw identification and exploitation
• API security testing and endpoint enumeration
• Session management and access control evaluation

Tools and Methodologies:
• Burp Suite Professional for manual testing
• OWASP ZAP for automated vulnerability scanning
• Gobuster for directory and subdomain enumeration
• Custom Python scripts for specific test cases
• Postman for API security testing

Findings and Impact:
• Discovered 8 high-severity vulnerabilities including SQL injection
• Identified authentication bypass in admin panel
• Found sensitive data exposure in API responses
• Provided detailed remediation guidance with code examples
• Conducted developer training on secure coding practices

The assessment led to significant improvements in the organization's application security posture and established ongoing security testing processes.''',
            'category': assessment_cat,
            'status': 'completed',
            'start_date': date(2023, 11, 1),
            'end_date': date(2023, 12, 15),
            'github_url': 'https://github.com/Christopher-Erick/web-app-security-tools',
            'technologies': ['Burp Suite', 'OWASP', 'Gobuster', 'Python', 'Nmap'],
            'is_featured': True
        },
        {
            'title': 'Security Automation & Incident Response Scripts',
            'slug': 'security-automation-scripts',
            'short_description': 'Collection of Python and Bash scripts for automated security tasks, vulnerability scanning, and incident response workflows.',
            'description': '''Developed a comprehensive suite of automation scripts to streamline security operations and improve incident response capabilities.

Script Categories:

1. Vulnerability Scanning Automation:
• Automated Nmap scanning with custom reporting
• Nessus API integration for scheduled scans
• Vulnerability database correlation and analysis
• Custom risk scoring algorithms

2. Log Analysis and Monitoring:
• Real-time log parsing for security events
• Anomaly detection using statistical analysis
• Automated threat hunting queries
• Integration with SIEM platforms

3. Incident Response Automation:
• Network isolation scripts for compromised systems
• Automated evidence collection and preservation
• Memory dump analysis and artifact extraction
• Timeline generation for forensic investigation

4. Compliance and Reporting:
• Automated compliance checks for security standards
• Report generation for management and auditors
• Metric collection and dashboard updates
• Policy violation detection and alerting

Technical Implementation:
• Python for data analysis and API integrations
• Bash scripting for system-level operations
• PowerShell for Windows environment automation
• REST API development for tool integrations

The automation suite reduced manual security tasks by 60% and improved consistency in security operations procedures.''',
            'category': automation_cat,
            'status': 'completed',
            'start_date': date(2024, 2, 1),
            'end_date': date(2024, 3, 30),
            'github_url': 'https://github.com/Christopher-Erick/security-automation-toolkit',
            'technologies': ['Python', 'Bash', 'PowerShell', 'Nmap', 'Nessus'],
            'is_featured': True
        },
        {
            'title': 'Malware Analysis Laboratory Setup',
            'slug': 'malware-analysis-lab',
            'short_description': 'Isolated malware analysis environment with dynamic and static analysis capabilities for investigating suspicious files and executables.',
            'description': '''Established a comprehensive malware analysis laboratory for investigating suspicious files, executables, and potential threats in a secure, isolated environment.

Laboratory Components:

1. Infrastructure Setup:
• VMware ESXi hypervisor with isolated network segments
• Windows and Linux analysis virtual machines
• Network simulation and traffic capture capabilities
• Sandbox environments for safe malware execution

2. Static Analysis Tools:
• PE file analysis using PEStudio and Detect It Easy
• Disassembly and decompilation with IDA Pro and Ghidra
• String analysis and entropy calculation tools
• Hash verification and VirusTotal integration

3. Dynamic Analysis Platform:
• Process monitoring with Process Monitor and API Monitor
• Network traffic analysis using Wireshark and TCPView
• Registry and file system change tracking
• Memory dump analysis with Volatility framework

4. Automation and Reporting:
• Python scripts for automated analysis workflows
• Behavioral analysis report generation
• Threat intelligence correlation and IOC extraction
• Integration with threat hunting platforms

Analysis Capabilities:
• Identification of malware families and variants
• Command and control (C2) infrastructure analysis
• Payload extraction and decryption techniques
• Persistence mechanism identification
• Anti-analysis technique detection and bypass

Sample Analysis Results:
• Successfully analyzed 25+ malware samples
• Identified new variants of known malware families
• Extracted network indicators of compromise (IOCs)
• Developed YARA rules for threat detection
• Contributed findings to threat intelligence platforms''',
            'category': malware_cat,
            'status': 'development',
            'start_date': date(2024, 4, 1),
            'end_date': None,
            'technologies': ['Kali Linux', 'Python', 'Wireshark', 'OWASP'],
            'is_featured': False
        }
    ]
    
    for project_data in projects:
        # Extract technologies list
        tech_names = project_data.pop('technologies')
        
        # Create project
        project, created = Project.objects.get_or_create(
            slug=project_data['slug'],
            defaults=project_data
        )
        
        if created:
            print(f"Created project: {project.title}")
            
            # Add technologies
            for tech_name in tech_names:
                try:
                    tech = Technology.objects.get(name=tech_name)
                    project.technologies.add(tech)
                except Technology.DoesNotExist:
                    print(f"Technology '{tech_name}' not found")
            
            project.save()


def create_project_features():
    """Create features for projects"""
    
    # Features for Enterprise Network Penetration Testing
    try:
        pentest_project = Project.objects.get(slug='enterprise-network-pentest')
        features = [
            {
                'title': 'External Perimeter Testing',
                'description': 'Comprehensive testing of external-facing services and applications',
                'icon': 'fas fa-globe',
                'order': 1
            },
            {
                'title': 'Internal Network Assessment',
                'description': 'Detailed analysis of internal network segmentation and security controls',
                'icon': 'fas fa-network-wired',
                'order': 2
            },
            {
                'title': 'Privilege Escalation',
                'description': 'Demonstration of privilege escalation techniques and lateral movement',
                'icon': 'fas fa-arrow-up',
                'order': 3
            },
            {
                'title': 'Detailed Reporting',
                'description': 'Comprehensive report with findings, risk ratings, and remediation guidance',
                'icon': 'fas fa-file-alt',
                'order': 4
            }
        ]
        
        for feature_data in features:
            feature_data['project'] = pentest_project
            ProjectFeature.objects.get_or_create(
                project=pentest_project,
                title=feature_data['title'],
                defaults=feature_data
            )
    except Project.DoesNotExist:
        pass
    
    # Features for Wazuh SIEM Implementation
    try:
        siem_project = Project.objects.get(slug='wazuh-siem-implementation')
        features = [
            {
                'title': 'Real-time Monitoring',
                'description': 'Continuous monitoring of security events across all endpoints',
                'icon': 'fas fa-eye',
                'order': 1
            },
            {
                'title': 'Custom Rule Development',
                'description': 'Advanced detection rules tailored to specific threat scenarios',
                'icon': 'fas fa-cogs',
                'order': 2
            },
            {
                'title': 'Automated Response',
                'description': 'Immediate response to security incidents through automated playbooks',
                'icon': 'fas fa-robot',
                'order': 3
            },
            {
                'title': 'Compliance Reporting',
                'description': 'Automated compliance reports for security frameworks and standards',
                'icon': 'fas fa-chart-bar',
                'order': 4
            }
        ]
        
        for feature_data in features:
            feature_data['project'] = siem_project
            ProjectFeature.objects.get_or_create(
                project=siem_project,
                title=feature_data['title'],
                defaults=feature_data
            )
    except Project.DoesNotExist:
        pass


def main():
    """Main function to create all portfolio data"""
    print("Creating portfolio data...")
    
    print("\n1. Creating categories...")
    create_categories()
    
    print("\n2. Creating technologies...")
    create_technologies()
    
    print("\n3. Creating projects...")
    create_projects()
    
    print("\n4. Creating project features...")
    create_project_features()
    
    print("\nPortfolio data creation completed!")
    print(f"Total categories: {Category.objects.count()}")
    print(f"Total technologies: {Technology.objects.count()}")
    print(f"Total projects: {Project.objects.count()}")
    print(f"Featured projects: {Project.objects.filter(is_featured=True).count()}")


if __name__ == '__main__':
    main()