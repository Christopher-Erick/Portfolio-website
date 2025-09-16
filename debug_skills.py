from main.models import Skill
from collections import defaultdict

# Get all skills
skills = Skill.objects.all()
print(f"Total skills: {skills.count()}")

# Check categories
categories = set()
for skill in skills:
    categories.add(skill.category)
print(f"Categories in database: {categories}")

# Apply the same logic as in the view
skills_by_category = defaultdict(list)
category_mapping = {
    'frontend': 'tools',
    'backend': 'tools',
    'database': 'tools',
    'tools': 'tools',
    'soft': 'specialized',
}

for skill in skills:
    mapped_category = category_mapping.get(skill.category, skill.category)
    skills_by_category[mapped_category].append(skill)

print(f"Skills by category: {dict(skills_by_category)}")
print(f"Categories after mapping: {list(skills_by_category.keys())}")