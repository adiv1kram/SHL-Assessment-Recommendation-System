#!/usr/bin/env python3
"""
Script to add descriptions to SHL assessments that don't have them.
Generates contextual descriptions based on assessment names and test types.
"""
import json

def generate_description(name, test_types):
    """Generate a contextual description based on assessment name and type"""
    
    # Common patterns
    descriptions = {
        "manager": "Evaluates management capabilities including leadership, decision-making, strategic thinking, and team oversight skills",
        "administrative": "Assesses organizational skills, attention to detail, multitasking ability, and administrative competencies",
        "professional": "Measures professional aptitude, workplace behavior, and job-specific competencies",
        "supervisor": "Tests supervisory skills including team management, performance monitoring, and operational oversight",
        "agent": "Evaluates customer service skills, communication abilities, and problem-solving in client-facing roles",
        "clerk": "Assesses clerical proficiency, data entry accuracy, organizational skills, and administrative support capabilities",
        "assistant": "Measures support skills, coordination abilities, and capacity to assist in professional environments",
        "apprentice": "Evaluates foundational job skills, learning potential, and readiness for apprenticeship programs",
        "collection": "Tests debt collection skills, negotiation abilities, and customer interaction in financial recovery",
        "bank": "Assesses banking industry knowledge, financial acumen, and customer service in financial institutions",
        "bookkeeping": "Evaluates accounting skills, numerical accuracy, financial record-keeping, and analytical abilities",
        "accounting": "Tests accounting principles, financial analysis, reporting capabilities, and numerical reasoning",
        "auditing": "Measures audit skills, attention to detail, compliance knowledge, and analytical thoroughness",
        "bilingual": "Assesses multilingual communication skills, cultural competency, and language proficiency",
        "reservation": "Tests booking management, customer service, scheduling abilities, and hospitality skills",
        "sales": "Evaluates sales techniques, customer persuasion, relationship building, and revenue generation skills",
        "service": "Measures customer service excellence, problem resolution, and client satisfaction capabilities",
        "technical": "Assesses technical knowledge, problem-solving abilities, and domain-specific expertise",
        "developer": "Tests programming skills, software development capabilities, and technical problem-solving",
        "analyst": "Evaluates analytical thinking, data interpretation, and strategic insight abilities"
    }
    
    name_lower = name.lower()
    
    # Find matching description
    for keyword, desc in descriptions.items():
        if keyword in name_lower:
            # Customize based on test types
            if test_types:
                type_str = ", ".join(test_types)
                return f"{desc}. Assessment includes: {type_str}."
            return f"{desc}."
    
    # Default description
    if test_types:
        type_str = ", ".join(test_types)
        return f"Comprehensive assessment measuring {name} competencies. Includes: {type_str}."
    return f"Pre-packaged assessment solution for {name} roles measuring relevant job competencies."

def main():
    # Load current catalog
    with open('shl_catalog.json', 'r') as f:
        catalog = json.load(f)
    
    # Backup original
    with open('shl_catalog_backup.json', 'w') as f:
        json.dump(catalog, f, indent=2)
    print(f"✅ Backup saved to shl_catalog_backup.json")
    
    # Update descriptions
    updated_count = 0
    for item in catalog:
        if item.get('description') == 'No description available.':
            item['description'] = generate_description(
                item.get('name', ''),
                item.get('test_type', [])
            )
            updated_count += 1
    
    # Save updated catalog
    with open('shl_catalog.json', 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"✅ Updated {updated_count} assessments with descriptions")
    print(f"✅ Saved to shl_catalog.json")
    print(f"\n📊 Total assessments: {len(catalog)}")

if __name__ == "__main__":
    main()
