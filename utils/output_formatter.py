
import json


def format_as_json(data, pretty = True):
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def format_as_markdown(data):
    md_lines = []
    
    # Title
    title = data.get('title', 'Untitled Research Article')
    md_lines.append(f"# {title}\n")
    
    # Metadata
    md_lines.append("## Metadata\n")
    if data.get('authors'):
        md_lines.append(f"**Authors:** {data['authors']}\n")
    if data.get('journal'):
        md_lines.append(f"**Journal:** {data['journal']}\n")
    if data.get('year'):
        md_lines.append(f"**Year:** {data['year']}\n")
    if data.get('doi'):
        md_lines.append(f"**DOI:** {data['doi']}\n")
    
    # Abstract
    if data.get('abstract'):
        md_lines.append("\n## Abstract\n")
        md_lines.append(f"{data['abstract']}\n")
    
    # Background
    if data.get('background'):
        md_lines.append("\n## Background\n")
        md_lines.append(f"{data['background'].get('summary', '')}\n")
        if data['background'].get('key_points'):
            md_lines.append("\n**Key Points:**\n")
            for point in data['background']['key_points']:
                md_lines.append(f"- {point}\n")
    
    # Methods
    if data.get('methods'):
        md_lines.append("\n## Methods\n")
        md_lines.append(f"{data['methods'].get('summary', '')}\n")
        if data['methods'].get('key_points'):
            md_lines.append("\n**Key Techniques:**\n")
            for point in data['methods']['key_points']:
                md_lines.append(f"- {point}\n")
    
    # Results
    if data.get('results'):
        md_lines.append("\n## Results\n")
        md_lines.append(f"{data['results'].get('summary', '')}\n")
        if data['results'].get('key_points'):
            md_lines.append("\n**Key Findings:**\n")
            for point in data['results']['key_points']:
                md_lines.append(f"- {point}\n")
    
    # Conclusions
    if data.get('conclusions'):
        md_lines.append("\n## Conclusions\n")
        md_lines.append(f"{data['conclusions'].get('summary', '')}\n")
        if data['conclusions'].get('key_points'):
            md_lines.append("\n**Key Takeaways:**\n")
            for point in data['conclusions']['key_points']:
                md_lines.append(f"- {point}\n")
    
    return ''.join(md_lines)


def create_downloadable_json(data, filename = "research_article"):
    json_content = format_as_json(data, pretty=True)
    return json_content, f"{filename}.json"


def create_downloadable_markdown(data, filename = "research_article"):
    md_content = format_as_markdown(data)
    return md_content, f"{filename}.md"
