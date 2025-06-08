import os
import re
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle


class DataManager:
    def __init__(self, knowledge_base_path: str = "data/knowledge_base.txt"):
        self.knowledge_base_path = knowledge_base_path
        self.documents = []
        self.embeddings = None
        self.model = None
        self.embeddings_cache_path = "data/embeddings_cache.pkl"
        self.load_data()
    
    def load_data(self):
        """Load and parse the knowledge base from text file"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Split content by section separators (---) or by ## headers
            # First, remove the main header if it exists
            lines = content.split('\n')
            processed_lines = []
            skip_main_header = True
            
            for line in lines:
                if line.startswith('# ') and skip_main_header:
                    skip_main_header = False
                    continue
                if line.strip():  # Skip empty lines after main header
                    skip_main_header = False
                    processed_lines.append(line)
                elif not skip_main_header:
                    processed_lines.append(line)
            
            content = '\n'.join(processed_lines)
            
            # Split by section separators (---)
            sections = re.split(r'\n---\n', content)
            
            for section in sections:
                section = section.strip()
                if section:  # Process any non-empty section
                    # Extract title and content
                    lines = section.split('\n')
                    title = ""
                    content_text = ""
                    source = ""
                    
                    for line in lines:
                        if line.startswith('## '):
                            title = line.replace('## ', '').strip()
                        elif line.startswith('Source: '):
                            source = line.replace('Source: ', '').strip()
                        elif line.strip() and not line.startswith('#') and not line.startswith('Source: '):
                            content_text += line.strip() + " "
                    
                    if title and content_text:
                        self.documents.append({
                            'title': title,
                            'content': content_text.strip(),
                            'source': source,
                            'full_text': f"{title}: {content_text.strip()}"
                        })
            
            print(f"Loaded {len(self.documents)} documents from knowledge base")
            if len(self.documents) > 0:
                print("Document titles:", [doc['title'] for doc in self.documents])
            self.initialize_embeddings()
            
        except FileNotFoundError:
            print(f"Knowledge base file not found: {self.knowledge_base_path}")
            self.documents = []
    
    def initialize_embeddings(self):
        """Initialize the sentence transformer model and create embeddings"""
        print("Initializing sentence transformer model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Check if cached embeddings exist
        if os.path.exists(self.embeddings_cache_path):
            try:
                with open(self.embeddings_cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                    if len(cached_data['embeddings']) == len(self.documents):
                        self.embeddings = cached_data['embeddings']
                        print("Loaded cached embeddings")
                        return
            except Exception as e:
                print(f"Error loading cached embeddings: {e}")
        
        # Create new embeddings
        print("Creating embeddings for documents...")
        texts = [doc['full_text'] for doc in self.documents]
        self.embeddings = self.model.encode(texts)
        
        # Cache the embeddings
        try:
            os.makedirs(os.path.dirname(self.embeddings_cache_path), exist_ok=True)
            with open(self.embeddings_cache_path, 'wb') as f:
                pickle.dump({
                    'embeddings': self.embeddings,
                    'document_count': len(self.documents)
                }, f)
            print("Embeddings cached successfully")
        except Exception as e:
            print(f"Error caching embeddings: {e}")
    
    def search_similar_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for similar documents using semantic similarity"""
        if not self.model or self.embeddings is None or len(self.documents) == 0:
            return []
        
        # Create embedding for the query
        query_embedding = self.model.encode([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Threshold for relevance
                doc = self.documents[idx].copy()
                doc['similarity_score'] = float(similarities[idx])
                results.append(doc)
        
        return results
    
    def get_context_for_query(self, query: str, max_context_length: int = 1500) -> Tuple[str, List[str]]:
        """Get relevant context and sources for a query"""
        relevant_docs = self.search_similar_documents(query, top_k=3)
        
        if not relevant_docs:
            return "", []
        
        context_parts = []
        sources = []
        current_length = 0
        
        for doc in relevant_docs:
            doc_text = f"**{doc['title']}**\n{doc['content']}\n"
            
            if current_length + len(doc_text) <= max_context_length:
                context_parts.append(doc_text)
                if doc['source']:
                    sources.append(doc['source'])
                current_length += len(doc_text)
            else:
                break
        
        context = "\n".join(context_parts)
        return context, sources
    
    def add_document(self, title: str, content: str, source: str = ""):
        """Add a new document to the knowledge base"""
        new_doc = {
            'title': title,
            'content': content,
            'source': source,
            'full_text': f"{title}: {content}"
        }
        
        self.documents.append(new_doc)
        
        # Update embeddings
        if self.model:
            new_embedding = self.model.encode([new_doc['full_text']])
            if self.embeddings is not None:
                self.embeddings = np.vstack([self.embeddings, new_embedding])
            else:
                self.embeddings = new_embedding


def load_knowledge_base(file_path: str) -> str:
    """Legacy function for backward compatibility"""
    with open(file_path, 'r') as file:
        knowledge_base = file.read()
    return knowledge_base

def log_chat(file_path: str, log_entry: str) -> None:
    """Log chat interactions"""
    with open(file_path, 'a') as file:
        file.write(log_entry + '\n')
