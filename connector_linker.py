import re
import sys

def extract_connectors(markdown):
    # Extract all connectors from subheaders
    connectors = re.findall(r'### ([CG]\d+)', markdown)
    return set(connectors)

def find_connector_rows(markdown):
    # Find all connector rows in the table and extract connectors
    rows = re.findall(r'\|.*?\|.*?\|.*?\|.*?\|', markdown)
    connector_rows = set()
    for row in rows:
        matches = re.findall(r'\b([CG]\d+)(/P\d+)?\b', row)
        for match in matches:
            connector_rows.add(match[0])
    return connector_rows

def add_links(markdown, valid_connectors):
    def replace_links(match):
        connector, pin = match.groups()
        if connector in valid_connectors:
            if pin:
                return f'[{connector}{pin}](#{connector.lower()})'
            else:
                return f'[{connector}](#{connector.lower()})'
        else:
            return f'{connector}{pin}' if pin else connector
    
    pattern = re.compile(r'(\b[CG]\d+)(/P\d+)?\b')
    linked_markdown = pattern.sub(replace_links, markdown)
    
    return linked_markdown

def process_file(filename):
    with open(filename, 'r') as file:
        markdown_content = file.read()
    
    # Extract valid connectors from subheaders
    valid_connectors = extract_connectors(markdown_content)
    print("Connector headers found:")
    for connector in valid_connectors:
        print(connector)
    
    # Find all connector rows
    connector_rows = find_connector_rows(markdown_content)
    print("\nConnector rows found:")
    for connector in connector_rows:
        print(connector)
    
    # Add links only to valid connectors
    linked_markdown = add_links(markdown_content, valid_connectors)
    
    output_filename = filename.replace('.md', '_linked.md')
    with open(output_filename, 'w') as output_file:
        output_file.write(linked_markdown)
    
    print(f"\nProcessed file saved as {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    process_file(filename)
