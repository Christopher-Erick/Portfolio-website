#!/usr/bin/env python
"""
Script to populate all portfolio data including personal information, projects, and resume details
"""
import os
import sys
import django
from datetime import date

# Check if script should run based on environment variable
if os.environ.get('RUN_POPULATE_SCRIPT', '').lower() != 'true':
    print("ℹ️  Populate script skipped. Set RUN_POPULATE_SCRIPT=true to run.")
    sys.exit(0)

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.contrib.auth import get_user_model
from main.models import Skill, Experience, Education, Certification, Achievement, Testimonial
from portfolio.models import Category, Technology, Project, ProjectFeature
from config import PersonalConfig

# Get User model
User = get_user_model()


def check_existing_data():
    """Check if there's existing data in the database"""
    # Using getattr to handle linter false positives
    try:
        has_data = any([
            getattr(Skill, 'objects').exists(),
            getattr(Experience, 'objects').exists(),
            getattr(Education, 'objects').exists(),
            getattr(Certification, 'objects').exists(),
            getattr(Achievement, 'objects').exists(),
            getattr(Testimonial, 'objects').exists(),
            getattr(Category, 'objects').exists(),
            getattr(Technology, 'objects').exists(),
            getattr(Project, 'objects').exists(),
        ])
        return has_data
    except AttributeError:
        # Handle case where linter doesn't recognize objects manager
        return False


def create_user_profile(update_existing=False):
    """Create or update user profile with personal information"""
    print("🔧 Creating/updating user profile...")
    
    # Get or create superuser
    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', PersonalConfig.get_email())
    
    user, created = getattr(User, 'objects').get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': PersonalConfig.get_full_name().split()[0],
            'last_name': ' '.join(PersonalConfig.get_full_name().split()[1:]) if len(PersonalConfig.get_full_name().split()) > 1 else '',
            'is_superuser': True,
            'is_staff': True
        }
    )
    
    if created:
        # Set a default password if user was created
        user.set_password('temp_password_change_me')
        user.save()
        print(f"✅ Created superuser: {username}")
    else:
        print(f"ℹ️ User {username} already exists")
        if update_existing:
            # Update user information if requested
            user.email = email
            user.first_name = PersonalConfig.get_full_name().split()[0]
            user.last_name = ' '.join(PersonalConfig.get_full_name().split()[1:]) if len(PersonalConfig.get_full_name().split()) > 1 else ''
            user.save()
            print(f"🔄 Updated user profile: {username}")


def create_skills(update_existing=False):
    """Create professional skills"""
    print("🔧 Creating skills...")
    
    skills_data = [
        # Technical Skills
        {'name': 'Penetration Testing', 'category': 'skill', 'proficiency': 95, 'icon': 'fas fa-bug'},
        {'name': 'Vulnerability Assessment', 'category': 'skill', 'proficiency': 90, 'icon': 'fas fa-shield-alt'},
        {'name': 'SIEM', 'category': 'skill', 'proficiency': 85, 'icon': 'fas fa-eye'},
        {'name': 'Incident Response', 'category': 'skill', 'proficiency': 88, 'icon': 'fas fa-bolt'},
        {'name': 'Network Security', 'category': 'skill', 'proficiency': 92, 'icon': 'fas fa-network-wired'},
        {'name': 'Web Application Security', 'category': 'skill', 'proficiency': 90, 'icon': 'fas fa-globe'},
        {'name': 'Malware Analysis', 'category': 'skill', 'proficiency': 80, 'icon': 'fas fa-virus'},
        {'name': 'Forensics', 'category': 'skill', 'proficiency': 75, 'icon': 'fas fa-search'},
        
        # Tools
        {'name': 'Kali Linux', 'category': 'tools', 'proficiency': 95, 'icon': 'fab fa-linux'},
        {'name': 'Wireshark', 'category': 'tools', 'proficiency': 90, 'icon': 'fas fa-chart-line'},
        {'name': 'Nmap', 'category': 'tools', 'proficiency': 95, 'icon': 'fas fa-map'},
        {'name': 'Metasploit', 'category': 'tools', 'proficiency': 85, 'icon': 'fas fa-bomb'},
        {'name': 'Burp Suite', 'category': 'tools', 'proficiency': 90, 'icon': 'fas fa-spider'},
        {'name': 'Nessus', 'category': 'tools', 'proficiency': 85, 'icon': 'fas fa-search'},
        {'name': 'Wazuh', 'category': 'tools', 'proficiency': 80, 'icon': 'fas fa-eye'},
        {'name': 'Splunk', 'category': 'tools', 'proficiency': 75, 'icon': 'fas fa-search-plus'},
        {'name': 'Gobuster', 'category': 'tools', 'proficiency': 85, 'icon': 'fas fa-spider'},
        
        # Soft Skills
        {'name': 'Problem Solving', 'category': 'soft', 'proficiency': 95, 'icon': 'fas fa-puzzle-piece'},
        {'name': 'Communication', 'category': 'soft', 'proficiency': 90, 'icon': 'fas fa-comments'},
        {'name': 'Team Leadership', 'category': 'soft', 'proficiency': 85, 'icon': 'fas fa-users'},
        {'name': 'Risk Assessment', 'category': 'soft', 'proficiency': 90, 'icon': 'fas fa-exclamation-triangle'},
        {'name': 'Documentation', 'category': 'soft', 'proficiency': 88, 'icon': 'fas fa-file-alt'},
    ]
    
    for skill_data in skills_data:
        try:
            skill, created = getattr(Skill, 'objects').get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                print(f"✅ Created skill: {skill.name}")
            else:
                print(f"ℹ️ Skill {skill.name} already exists")
                if update_existing:
                    # Update existing skill if requested
                    for key, value in skill_data.items():
                        setattr(skill, key, value)
                    skill.save()
                    print(f"🔄 Updated skill: {skill.name}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process skill {skill_data['name']}")


def create_experience(update_existing=False):
    """Create professional experience"""
    print("🔧 Creating experience...")
    
    experience_data = [
        {
            'company': 'Freelance Cybersecurity Consultant',
            'position': 'Senior Security Analyst',
            'start_date': date(2022, 1, 1),
            'end_date': None,  # Current position
            'description': 'Providing comprehensive cybersecurity services including penetration testing, vulnerability assessments, and security architecture consulting for clients across various industries.',
            'technologies': 'Kali Linux, Burp Suite, Nmap, Metasploit, Nessus, Wireshark'
        },
        {
            'company': 'TechSecure Solutions',
            'position': 'Cybersecurity Specialist',
            'start_date': date(2020, 6, 1),
            'end_date': date(2021, 12, 31),
            'description': 'Conducted security assessments, implemented security controls, and developed incident response procedures for enterprise clients. Managed SIEM platform and performed forensic investigations.',
            'technologies': 'Splunk, Wazuh, Python, Bash, ISO 27001, NIST'
        }
    ]
    
    for exp_data in experience_data:
        try:
            exp, created = getattr(Experience, 'objects').get_or_create(
                company=exp_data['company'],
                position=exp_data['position'],
                start_date=exp_data['start_date'],
                defaults=exp_data
            )
            if created:
                print(f"✅ Created experience: {exp.position} at {exp.company}")
            else:
                print(f"ℹ️ Experience {exp.position} at {exp.company} already exists")
                if update_existing:
                    # Update existing experience if requested
                    for key, value in exp_data.items():
                        setattr(exp, key, value)
                    exp.save()
                    print(f"🔄 Updated experience: {exp.position} at {exp.company}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process experience at {exp_data['company']}")


def create_education(update_existing=False):
    """Create educational background"""
    print("🔧 Creating education...")
    
    education_data = [
        {
            'institution': 'Jomo Kenyatta University of Agriculture and Technology',
            'degree': 'BSc. Information Technology',
            'field_of_study': 'Cybersecurity',
            'start_date': date(2018, 9, 1),
            'end_date': date(2022, 6, 30),
            'gpa': 3.7,
            'description': 'Specialized in cybersecurity with focus on network security, cryptography, and digital forensics.',
            'icon': 'fas fa-graduation-cap'
        }
    ]
    
    for edu_data in education_data:
        try:
            edu, created = getattr(Education, 'objects').get_or_create(
                institution=edu_data['institution'],
                degree=edu_data['degree'],
                start_date=edu_data['start_date'],
                defaults=edu_data
            )
            if created:
                print(f"✅ Created education: {edu.degree} from {edu.institution}")
            else:
                print(f"ℹ️ Education {edu.degree} from {edu.institution} already exists")
                if update_existing:
                    # Update existing education if requested
                    for key, value in edu_data.items():
                        setattr(edu, key, value)
                    edu.save()
                    print(f"🔄 Updated education: {edu.degree} from {edu.institution}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process education at {edu_data['institution']}")


def create_certifications(update_existing=False):
    """Create professional certifications"""
    print("🔧 Creating certifications...")
    
    cert_data = [
        {
            'name': 'Certified Ethical Hacker (CEH)',
            'issuing_organization': 'EC-Council',
            'issue_date': date(2021, 3, 15),
            'expiry_date': date(2024, 3, 15),
            'credential_id': 'ECEH-123456',
            'credential_url': 'https://aspen.eccouncil.org/VerifyBadge?type=certification&a=ABCDE12345',
            'description': 'Certification in ethical hacking techniques and methodologies for identifying vulnerabilities in systems and networks.',
            'icon': 'fas fa-certificate'
        },
        {
            'name': 'CompTIA Security+',
            'issuing_organization': 'CompTIA',
            'issue_date': date(2020, 8, 20),
            'expiry_date': date(2023, 8, 20),
            'credential_id': 'SEC+12345678',
            'credential_url': 'https://www.certmetrics.com/comptia/public/transcript.aspx',
            'description': 'Foundational cybersecurity certification covering network security, compliance, and operational security.',
            'icon': 'fas fa-shield-alt'
        }
    ]
    
    for cert in cert_data:
        try:
            certification, created = getattr(Certification, 'objects').get_or_create(
                name=cert['name'],
                issuing_organization=cert['issuing_organization'],
                issue_date=cert['issue_date'],
                defaults=cert
            )
            if created:
                print(f"✅ Created certification: {certification.name}")
            else:
                print(f"ℹ️ Certification {certification.name} already exists")
                if update_existing:
                    # Update existing certification if requested
                    for key, value in cert.items():
                        setattr(certification, key, value)
                    certification.save()
                    print(f"🔄 Updated certification: {certification.name}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process certification {cert['name']}")


def create_achievements(update_existing=False):
    """Create professional achievements"""
    print("🔧 Creating achievements...")
    
    achievements_data = [
        {
            'title': 'TryHackMe Top 1%',
            'description': 'Ranked in the top 1% of TryHackMe users globally with over 500 rooms completed and 1000+ days streak.',
            'icon': 'fas fa-trophy',
            'technologies': 'TryHackMe, CTF, Cybersecurity',
            'order': 1,
            'is_active': True
        },
        {
            'title': 'HackTheBox Hall of Fame',
            'description': 'Featured in HackTheBox Hall of Fame for successfully compromising multiple machines and contributing to the community.',
            'icon': 'fas fa-medal',
            'technologies': 'HackTheBox, Penetration Testing, CTF',
            'order': 2,
            'is_active': True
        },
        {
            'title': 'Bug Bounty Hunter',
            'description': 'Successfully identified and reported critical vulnerabilities to multiple organizations through responsible disclosure programs.',
            'icon': 'fas fa-bug',
            'technologies': 'Bug Bounty, Vulnerability Assessment, Web Security',
            'order': 3,
            'is_active': True
        }
    ]
    
    for ach_data in achievements_data:
        try:
            achievement, created = getattr(Achievement, 'objects').get_or_create(
                title=ach_data['title'],
                defaults=ach_data
            )
            if created:
                print(f"✅ Created achievement: {achievement.title}")
            else:
                print(f"ℹ️ Achievement {achievement.title} already exists")
                if update_existing:
                    # Update existing achievement if requested
                    for key, value in ach_data.items():
                        setattr(achievement, key, value)
                    achievement.save()
                    print(f"🔄 Updated achievement: {achievement.title}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process achievement {ach_data['title']}")


def create_testimonials(update_existing=False):
    """Create client testimonials"""
    print("🔧 Creating testimonials...")
    
    testimonials_data = [
        {
            'name': 'John Smith',
            'position': 'CTO',
            'company': 'TechCorp Ltd',
            'content': 'Christopher provided exceptional penetration testing services for our infrastructure. His thorough approach and detailed reporting helped us identify and remediate critical vulnerabilities before they could be exploited.',
            'is_active': True,
            'order': 1
        },
        {
            'name': 'Sarah Johnson',
            'position': 'Security Manager',
            'company': 'SecureNet Inc',
            'content': 'Working with Christopher on our SIEM implementation was a game-changer. His expertise in security monitoring and incident response significantly improved our threat detection capabilities.',
            'is_active': True,
            'order': 2
        }
    ]
    
    for test_data in testimonials_data:
        try:
            testimonial, created = getattr(Testimonial, 'objects').get_or_create(
                name=test_data['name'],
                company=test_data['company'],
                defaults=test_data
            )
            if created:
                print(f"✅ Created testimonial from: {testimonial.name}")
            else:
                print(f"ℹ️ Testimonial from {testimonial.name} already exists")
                if update_existing:
                    # Update existing testimonial if requested
                    for key, value in test_data.items():
                        setattr(testimonial, key, value)
                    testimonial.save()
                    print(f"🔄 Updated testimonial from: {testimonial.name}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process testimonial from {test_data['name']}")


def create_portfolio_categories(update_existing=False):
    """Create portfolio categories"""
    print("🔧 Creating portfolio categories...")
    
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
        }
    ]
    
    for cat_data in categories:
        try:
            category, created = getattr(Category, 'objects').get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                print(f"✅ Created category: {category.name}")
            else:
                print(f"ℹ️ Category {category.name} already exists")
                if update_existing:
                    # Update existing category if requested
                    for key, value in cat_data.items():
                        setattr(category, key, value)
                    category.save()
                    print(f"🔄 Updated category: {category.name}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process category {cat_data['name']}")
        except Exception as e:
            # Handle DoesNotExist exception
            if "DoesNotExist" in str(e):
                print("⚠️ Category not found")
            else:
                raise


def create_technologies(update_existing=False):
    """Create technologies"""
    print("🔧 Creating technologies...")
    
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
        {'name': 'OWASP', 'icon': 'fas fa-shield-alt', 'color': '#000000'},
        {'name': 'NIST', 'icon': 'fas fa-certificate', 'color': '#0066CC'},
        {'name': 'ISO 27001', 'icon': 'fas fa-certificate', 'color': '#FF9500'}
    ]
    
    for tech_data in technologies:
        try:
            technology, created = getattr(Technology, 'objects').get_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            if created:
                print(f"✅ Created technology: {technology.name}")
            else:
                print(f"ℹ️ Technology {technology.name} already exists")
                if update_existing:
                    # Update existing technology if requested
                    for key, value in tech_data.items():
                        setattr(technology, key, value)
                    technology.save()
                    print(f"🔄 Updated technology: {technology.name}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process technology {tech_data['name']}")
        except Exception as e:
            # Handle DoesNotExist exception
            if "DoesNotExist" in str(e):
                print("⚠️ Technology not found")
            else:
                raise


def create_projects(update_existing=False):
    """Create portfolio projects"""
    print("🔧 Creating projects...")
    
    # Get categories
    try:
        pentest_cat = getattr(Category, 'objects').get(slug='penetration-testing')
        assessment_cat = getattr(Category, 'objects').get(slug='security-assessment')
        siem_cat = getattr(Category, 'objects').get(slug='siem-monitoring')
        automation_cat = getattr(Category, 'objects').get(slug='security-automation')
    except AttributeError:
        # Handle linter false positive
        print("⚠️ Could not access categories")
        return
    except Exception as e:
        # Handle DoesNotExist exception
        if "DoesNotExist" in str(e):
            print("❌ Error: Required categories not found")
        else:
            raise
        return
    
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
            'is_featured': True,
            'order': 1
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
            'is_featured': True,
            'order': 2
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
            'is_featured': True,
            'order': 3
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
            'is_featured': True,
            'order': 4
        }
    ]
    
    for project_data in projects:
        # Extract technologies list
        tech_names = project_data.pop('technologies')
        
        try:
            # Create project
            project, created = getattr(Project, 'objects').get_or_create(
                slug=project_data['slug'],
                defaults=project_data
            )
            
            if created:
                print(f"✅ Created project: {project.title}")
                
                # Add technologies
                for tech_name in tech_names:
                    try:
                        tech = getattr(Technology, 'objects').get(name=tech_name)
                        project.technologies.add(tech)
                    except AttributeError:
                        # Handle linter false positive
                        print(f"⚠️ Could not add technology '{tech_name}' to project")
                    except Exception as e:
                        # Handle DoesNotExist exception
                        if "DoesNotExist" in str(e):
                            print(f"⚠️ Technology '{tech_name}' not found")
                        else:
                            raise
                
                project.save()
            else:
                print(f"ℹ️ Project {project.title} already exists")
                if update_existing:
                    # Update existing project if requested
                    for key, value in project_data.items():
                        setattr(project, key, value)
                    project.save()
                    
                    # Update technologies
                    project.technologies.clear()
                    for tech_name in tech_names:
                        try:
                            tech = getattr(Technology, 'objects').get(name=tech_name)
                            project.technologies.add(tech)
                        except AttributeError:
                            # Handle linter false positive
                            print(f"⚠️ Could not add technology '{tech_name}' to project")
                        except Exception as e:
                            # Handle DoesNotExist exception
                            if "DoesNotExist" in str(e):
                                print(f"⚠️ Technology '{tech_name}' not found")
                            else:
                                raise
                    
                    project.save()
                    print(f"🔄 Updated project: {project.title}")
        except AttributeError:
            # Handle linter false positive
            print(f"⚠️ Could not process project {project_data['title']}")
        except Exception as e:
            # Handle DoesNotExist exception
            if "DoesNotExist" in str(e):
                print(f"⚠️ Could not process project {project_data['title']}")
            else:
                raise


def main(update_existing=False):
    """Main function to populate all data"""
    print("🚀 Starting data population...")
    
    # Check if there's existing data
    has_existing_data = check_existing_data()
    
    if has_existing_data:
        print("⚠️  Existing data detected in the database")
        if not update_existing:
            print("ℹ️  Skipping data population to avoid duplication. Use --update to force update.")
            return
    
    try:
        create_user_profile(update_existing)
        print()
        
        create_skills(update_existing)
        print()
        
        create_experience(update_existing)
        print()
        
        create_education(update_existing)
        print()
        
        create_certifications(update_existing)
        print()
        
        create_achievements(update_existing)
        print()
        
        create_testimonials(update_existing)
        print()
        
        create_portfolio_categories(update_existing)
        print()
        
        create_technologies(update_existing)
        print()
        
        create_projects(update_existing)
        print()
        
        print("🎉 All data populated successfully!")
        print("\n📊 Summary:")
        print(f"  - Users: {getattr(User, 'objects').count()}")
        print(f"  - Skills: {getattr(Skill, 'objects').count()}")
        print(f"  - Experience entries: {getattr(Experience, 'objects').count()}")
        print(f"  - Education entries: {getattr(Education, 'objects').count()}")
        print(f"  - Certifications: {getattr(Certification, 'objects').count()}")
        print(f"  - Achievements: {getattr(Achievement, 'objects').count()}")
        print(f"  - Testimonials: {getattr(Testimonial, 'objects').count()}")
        print(f"  - Portfolio categories: {getattr(Category, 'objects').count()}")
        print(f"  - Technologies: {getattr(Technology, 'objects').count()}")
        print(f"  - Projects: {getattr(Project, 'objects').count()}")
        print(f"  - Featured projects: {getattr(Project, 'objects').filter(is_featured=True).count()}")
        
    except Exception as e:
        print(f"❌ Error populating data: {e}")
        raise


if __name__ == '__main__':
    # Check for command line arguments
    update_existing = '--update' in sys.argv
    main(update_existing)