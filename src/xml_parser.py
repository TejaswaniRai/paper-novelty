import xml.etree.ElementTree as ET
import csv
import re
from datetime import datetime

def parse_arxiv_xml(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace for arXiv
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'abstract', 'year', 'authors'])

        for entry in root.findall('atom:entry', ns):
            # Extract arXiv ID from the id tag
            id_elem = entry.find('atom:id', ns)
            if id_elem is None or id_elem.text is None:
                continue
            full_id = id_elem.text
            arxiv_id = full_id.split('/abs/')[-1] if '/abs/' in full_id else full_id.split('/')[-1]

            title_elem = entry.find('atom:title', ns)
            if title_elem is None or title_elem.text is None:
                title = ''
            else:
                title = title_elem.text.strip()

            summary_elem = entry.find('atom:summary', ns)
            if summary_elem is None or summary_elem.text is None:
                abstract = ''
            else:
                summary = summary_elem.text.strip()
                # Clean summary: remove extra whitespace
                abstract = ' '.join(summary.split())

            published_elem = entry.find('atom:published', ns)
            if published_elem is None or published_elem.text is None:
                year = 2023  # default
            else:
                published = published_elem.text
                try:
                    year = datetime.fromisoformat(published.replace('Z', '+00:00')).year
                except:
                    year = 2023

            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None and name_elem.text is not None:
                    authors.append(name_elem.text)
            authors_str = '; '.join(authors)

            writer.writerow([arxiv_id, title, abstract, year, authors_str])

if __name__ == '__main__':
    parse_arxiv_xml('../data/arxiv_data.xml', '../data/papers.csv')
    print("Parsed arxiv_data.xml into papers.csv")
