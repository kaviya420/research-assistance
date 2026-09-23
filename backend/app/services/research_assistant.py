from ai_engine.nlp.extraction import extract_text_from_pdf, chunk_text
from ai_engine.embeddings.vector_store import VectorStore
from ai_engine.summarizer.paper_summarizer import summarize_paper, analyze_papers
from ai_engine.clustering.topic_modeling import cluster_documents, group_papers_by_cluster
from ai_engine.rag.ollama_client import generate_completion
import uuid
import os
import numpy as np

class ResearchAssistantDatabase:
    def __init__(self):
        self.papers = []
        index_path = '../data/faiss_index.bin'
        meta_path = '../data/metadata.pkl'
        if os.path.exists(index_path): os.remove(index_path)
        if os.path.exists(meta_path): os.remove(meta_path)
        
        self.vector_store = VectorStore(index_path=index_path, metadata_path=meta_path)
        
    def process_pdf(self, filename: str, file_bytes: bytes):
        text = extract_text_from_pdf(file_bytes)
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF.")
            
        paper_id = str(uuid.uuid4())
        summary = summarize_paper(text)
        
        paper_record = {
            "id": paper_id,
            "filename": filename,
            "summary": summary
        }
        self.papers.append(paper_record)
        
        chunks = chunk_text(text)
        metadatas = [{"paper_id": paper_id, "filename": filename, "chunk_text": c} for c in chunks]
        self.vector_store.add_texts(chunks, metadatas)
        
        return paper_record

    def get_all_papers(self):
        return self.papers

    def delete_paper(self, paper_id: str):
        self.papers = [p for p in self.papers if p["id"] != paper_id]

    def _get_active_embeddings(self):
        active_ids = {p["id"] for p in self.papers}
        all_vecs, all_meta = self.vector_store.get_all_embeddings()
        
        if len(all_vecs) == 0:
            return [], []
            
        active_vecs = []
        active_meta = []
        for i, meta in enumerate(all_meta):
            if meta.get("paper_id") in active_ids:
                active_vecs.append(all_vecs[i])
                active_meta.append(meta)
                
        return np.array(active_vecs) if active_vecs else [], active_meta
        
    def perform_cross_paper_analysis(self):
        if len(self.papers) == 0:
            return {"clusters": [], "contradictions": "No papers available.", "research_gaps": "No papers available."}
            
        embeddings, metadatas = self._get_active_embeddings()
        if len(embeddings) == 0:
            return {"clusters": [], "contradictions": "No valid data to analyze.", "research_gaps": "No valid data."}
            
        num_clusters = min(3, max(1, len(list(set([m['paper_id'] for m in metadatas])))))
        doc_clusters = cluster_documents(embeddings, metadatas, num_clusters=num_clusters)
        
        clusters_map = group_papers_by_cluster(doc_clusters)
        
        formatted_clusters = []
        for c_id, docs in clusters_map.items():
            formatted_clusters.append({
                "cluster_name": f"Topic Group {c_id + 1}",
                "documents": list(set([d.get("filename") for d in docs]))[:5]
            })
            
        summaries = [p["summary"] for p in self.papers]
        analysis_result = analyze_papers(summaries)
        
        return {
            "clusters": formatted_clusters,
            "contradictions": analysis_result.get("contradictions", "None detected."),
            "research_gaps": analysis_result.get("research_gaps", "None detected.")
        }

    def chat_with_papers(self, query: str):
        if not self.papers:
            return "Please upload some papers to chat about."

        raw_results = self.vector_store.search(query, k=15)
        active_ids = {p["id"] for p in self.papers}
        
        valid_chunks = []
        for result in raw_results:
            if result["metadata"]["paper_id"] in active_ids:
                valid_chunks.append(f"[{result['metadata']['filename']}] {result['metadata']['chunk_text']}")
                
        valid_chunks = valid_chunks[:5]
        context_str = "\n".join(valid_chunks)
        
        prompt = f"""
You are an expert academic assistant. Use the following excerpts from the uploaded research papers to answer the user's question accurately.
If the answer is not contained within the context, calmly state that it cannot be found in the current documents.

CONTEXT:
{context_str}

USER QUESTION:
{query}

ANSWER:
"""
        response = generate_completion(prompt)
        return response

db = ResearchAssistantDatabase()
