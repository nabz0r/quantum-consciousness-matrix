import scholarly
import bibtexparser
import pandas as pd
import json
from typing import List, Dict

class LiteratureCollector:
    def __init__(self, keywords: List[str]):
        self.keywords = keywords
        self.collected_papers = []
        self.databases = [
            'google_scholar', 
            'scopus', 
            'web_of_science'
        ]
    
    def search_google_scholar(self, keyword: str, max_results: int = 50):
        """Search Google Scholar and collect paper metadata"""
        results = []
        search_query = scholarly.search_pubs(keyword)
        
        for _ in range(max_results):
            try:
                paper = next(search_query)
                results.append({
                    'title': paper.get('bib', {}).get('title', ''),
                    'authors': paper.get('bib', {}).get('author', []),
                    'year': paper.get('bib', {}).get('pub_year', None),
                    'citations': paper.get('num_citations', 0),
                    'source': 'Google Scholar'
                })
            except StopIteration:
                break
        
        return results

    def apply_selection_criteria(self, papers: List[Dict]) -> List[Dict]:
        """Apply rigorous selection criteria"""
        filtered_papers = []
        for paper in papers:
            # Example criteria - can be expanded
            if (paper['year'] and int(paper['year']) >= 2003 and  # Last 20 years
                paper['citations'] > 5 and  # Minimum citation threshold
                len(paper['title']) > 10):  # Meaningful title
                filtered_papers.append(paper)
        
        return filtered_papers

    def collect_literature(self):
        """Collect literature across multiple databases"""
        for keyword in self.keywords:
            # Google Scholar search
            scholar_results = self.search_google_scholar(keyword)
            filtered_results = self.apply_selection_criteria(scholar_results)
            
            self.collected_papers.extend(filtered_results)
    
    def export_results(self, format='json'):
        """Export collected literature"""
        if format == 'json':
            with open('literature_collection.json', 'w') as f:
                json.dump(self.collected_papers, f, indent=2)
        
        elif format == 'csv':
            df = pd.DataFrame(self.collected_papers)
            df.to_csv('literature_collection.csv', index=False)
        
        elif format == 'bibtex':
            # Convert to BibTeX
            bib_entries = []
            for paper in self.collected_papers:
                bib_entry = {
                    'title': paper['title'],
                    'author': ' and '.join(paper['authors']),
                    'year': str(paper['year']),
                }
                bib_entries.append(bib_entry)
            
            with open('literature_collection.bib', 'w') as f:
                bibtexparser.dump(bib_entries, f)

def main():
    keywords = [
        'quantum consciousness', 
        'emergent intelligence', 
        'neural complexity', 
        'cognitive quantum theory'
    ]
    
    collector = LiteratureCollector(keywords)
    collector.collect_literature()
    collector.export_results(format='json')
    collector.export_results(format='csv')
    collector.export_results(format='bibtex')

if __name__ == "__main__":
    main()

# Requirements:
# pip install scholarly pandas bibtexparser