"""
Specialized agents for the RAG system.
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

from .base import BaseAgent, Task, Result, Plan, Response

@dataclass
class QueryAnalysis:
    """Results of query analysis"""
    subtasks: List[Task]
    intents: List[str]
    domains: List[str]  # Added domains field
    tags: List[str]     # Added tags field
    context: Dict[str, Any]
    confidence: float
    timestamp: datetime = datetime.now()

@dataclass
class DocAnalysis:
    """Results of document analysis"""
    content: Any
    context: Dict[str, Any]
    relationships: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class QueryAnalysisAgent(BaseAgent):
    """
    Analyzes and decomposes user queries.
    """
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.add_capability("query_analysis")
        self.add_capability("intent_recognition")
        self.add_capability("context_analysis")

    async def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze and decompose a user query"""
        # Identify query intents and domains
        intents = await self._identify_intents(query)
        domains = await self._identify_domains(query)
        tags = await self._identify_tags(query)
        
        # Analyze query context
        context = await self._analyze_context(query)
        
        # Create subtasks based on identified domains
        subtasks = await self._create_subtasks(domains)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(subtasks, intents, context)
        
        return QueryAnalysis(
            subtasks=subtasks,
            intents=intents,
            domains=domains,
            tags=tags,
            context=context,
            confidence=confidence
        )

    async def _identify_domains(self, query: str) -> List[str]:
        """Identify relevant domains from the query"""
        domains = []
        
        # Define domain keywords
        domain_keywords = {
            "quantum": ["quantum", "qubit", "superposition", "entanglement"],
            "artificial": ["ai", "artificial intelligence", "machine learning", "neural network"],
            "climate": ["climate", "weather", "temperature", "greenhouse", "ocean", "marine"]
        }
        
        # Check for domain keywords in query
        query_lower = query.lower()
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                domains.append(domain)
        
        return domains

    async def _identify_tags(self, query: str) -> List[str]:
        """Identify relevant tags from the query"""
        tags = []
        
        # Map domains to tags
        domain_to_tags = {
            "quantum": ["quantum", "physics"],
            "artificial": ["ai", "machine-learning"],
            "climate": ["climate", "environment", "marine"]
        }
        
        # Get domains and add corresponding tags
        domains = await self._identify_domains(query)
        for domain in domains:
            if domain in domain_to_tags:
                tags.extend(domain_to_tags[domain])
        
        return list(set(tags))  # Remove duplicates

    async def _identify_intents(self, query: str) -> List[str]:
        """Identify intents in the query"""
        # Map common query patterns to intents
        intent_patterns = {
            "compare": ["compare", "contrast", "difference", "versus", "vs"],
            "explain": ["explain", "describe", "what is", "how does", "what are"],
            "analyze": ["analyze", "examine", "investigate"],
            "solve": ["solve", "address", "handle", "fix"],
            "impact": ["impact", "effect", "affect", "influence"]
        }
        
        query_lower = query.lower()
        intents = []
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                intents.append(intent)
        
        return intents if intents else ["explain"]  # Default to explain

    async def _create_subtasks(self, domains: List[str]) -> List[Task]:
        """Create subtasks based on identified domains"""
        tasks = []
        for i, domain in enumerate(domains):
            task = Task(
                id=f"analyze_domain_{domain}_{i}",
                type="document_analysis",
                data={"domain": domain},
                priority=1
            )
            tasks.append(task)
        return tasks

    async def _analyze_context(self, query: str) -> Dict[str, Any]:
        """Analyze query context"""
        return {
            "query_type": "comparison" if "compare" in query.lower() else "single_domain",
            "complexity": "complex" if len(query.split()) > 10 else "simple",
            "focus": self._identify_focus(query)
        }

    def _identify_focus(self, query: str) -> str:
        """Identify the main focus of the query"""
        focus_keywords = {
            "temperature": ["temperature", "warming", "heat"],
            "biodiversity": ["biodiversity", "species", "ecosystem"],
            "coral": ["coral", "reef"],
            "ocean": ["ocean", "sea", "marine"],
            "climate": ["climate", "weather", "atmospheric"]
        }
        
        query_lower = query.lower()
        for focus, keywords in focus_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return focus
        return "general"

    def _calculate_confidence(
        self,
        subtasks: List[Task],
        intents: List[str],
        context: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for the analysis"""
        # Base confidence
        confidence = 0.7
        
        # Adjust based on number of identified components
        if subtasks:
            confidence += 0.1
        if intents:
            confidence += 0.1
        if context:
            confidence += 0.1
            
        return min(confidence, 1.0)  # Cap at 1.0

class DocumentAgent(BaseAgent):
    """
    Manages document access and analysis.
    """
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.add_capability("document_analysis")
        self.add_capability("content_extraction")
        self.add_capability("relationship_mapping")

    async def analyze_document(self, doc_ref) -> DocAnalysis:
        """Analyze a document"""
        # Extract metadata from the document reference
        metadata = {
            "doc_id": doc_ref.metadata.doc_id,
            "filename": doc_ref.metadata.filename,
            "content_type": doc_ref.metadata.content_type,
            "tags": doc_ref.metadata.tags,
            "domain": doc_ref.metadata.additional_metadata.get("domain") or doc_ref.metadata.metadata.get("domain", "unknown")
        }
        
        # Retrieve actual document content
        content = await self._retrieve_content(doc_ref)
        
        # Extract context
        context = await self._extract_context(content, metadata)
        
        # Identify relationships
        relationships = await self._identify_relationships(content, metadata)
        
        return DocAnalysis(
            content=content,
            context=context,
            relationships=relationships,
            metadata=metadata
        )

    async def _retrieve_content(self, doc_ref) -> Any:
        """Retrieve document content"""
        try:
            # Get the actual content from the document store
            content = await doc_ref.doc_manager.retrieve_document(doc_ref.doc_id)
            if content is None:
                return f"Error: Content not found for {doc_ref.metadata.filename}"
            
            # Decode content based on content type
            if doc_ref.metadata.content_type.startswith('text/'):
                return content.decode('utf-8')
            else:
                return content
                
        except Exception as e:
            return f"Error retrieving content: {str(e)}"

    async def _extract_context(self, content: Any, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extract context from content"""
        context = {
            "domain": metadata.get("domain", "unknown"),
            "content_type": metadata.get("content_type", "unknown"),
            "summary": None,
            "key_points": [],
            "conclusions": None  # Added conclusions field
        }
        
        # Generate summary and extract key points for text content
        if isinstance(content, str):
            # Extract first paragraph as summary
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            if paragraphs:
                context["summary"] = paragraphs[0]
            
            # Extract key points (numbered or bulleted lists)
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith(('•', '-', '*')) or (len(line) > 0 and line[0].isdigit()):
                    context["key_points"].append(line.lstrip('•-* '))
            
            # Extract conclusions section
            conclusions_match = re.search(r'Conclusions?:(.+?)(?=\n\n|\Z)', content, re.DOTALL | re.IGNORECASE)
            if conclusions_match:
                context["conclusions"] = conclusions_match.group(1).strip()
            
        return context

    async def _identify_relationships(
        self,
        content: Any,
        metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify relationships in content"""
        relationships = []
        
        # Add domain relationship
        domain = metadata.get("domain", "unknown")
        relationships.append({
            "type": "domain",
            "value": domain
        })
        
        # Add tag relationships
        for tag in metadata.get("tags", []):
            relationships.append({
                "type": "tag",
                "value": tag
            })
            
        # Add content-based relationships
        if isinstance(content, str):
            # Look for related topics in content
            related_topics = {
                "temperature": ["temperature", "warming", "heat"],
                "biodiversity": ["biodiversity", "species", "ecosystem"],
                "coral": ["coral", "reef"],
                "ocean": ["ocean", "sea", "marine"]
            }
            
            content_lower = content.lower()
            for topic, keywords in related_topics.items():
                if any(keyword in content_lower for keyword in keywords):
                    relationships.append({
                        "type": "topic",
                        "value": topic
                    })
            
        return relationships

class SynthesisAgent(BaseAgent):
    """
    Synthesizes information from multiple sources.
    """
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.add_capability("information_synthesis")
        self.add_capability("response_generation")
        self.add_capability("source_attribution")

    async def synthesize(
        self,
        query: QueryAnalysis,
        documents: List[DocAnalysis],
        original_query: str = None
    ) -> Result:
        """Synthesize information from multiple sources"""
        # Extract relevant information
        relevant_info = await self._extract_relevant_info(query, documents, original_query)
        
        # Integrate information
        integrated_info = await self._integrate_information(relevant_info, original_query)
        
        # Generate response
        response = await self._generate_response(integrated_info, query.intents, original_query)
        
        # Calculate confidence
        confidence = self._calculate_confidence(documents, query)
        
        # Extract sources
        sources = [doc.metadata.get("filename") for doc in documents]
        
        return Result(
            task_id=f"synthesis_{datetime.now().timestamp()}",
            status="completed",
            data=response,
            error=None,
            completion_time=datetime.now(),
            metadata={
                "confidence": confidence,
                "sources": sources
            }
        )

    async def _extract_relevant_info(
        self,
        query: QueryAnalysis,
        documents: List[DocAnalysis],
        original_query: str = None
    ) -> List[Dict[str, Any]]:
        """Extract relevant information based on query"""
        relevant_info = []
        
        # Identify focus areas from the query
        focus_areas = set()
        if original_query:
            original_query_lower = original_query.lower()
            focus_mapping = {
                "temperature": ["temperature", "warming", "heat"],
                "biodiversity": ["biodiversity", "species", "ecosystem"],
                "coral": ["coral", "reef"],
                "ocean": ["ocean", "sea", "marine"],
                "conclusions": ["conclusion", "summary", "findings"]
            }
            
            for focus, keywords in focus_mapping.items():
                if any(keyword in original_query_lower for keyword in keywords):
                    focus_areas.add(focus)
        
        for doc in documents:
            if not isinstance(doc.content, str):
                continue
            
            # Create structured info with focus on relevant parts
            info = {
                "content": doc.content,
                "summary": doc.context.get("summary"),
                "domain": doc.context.get("domain"),
                "key_points": doc.context.get("key_points", []),
                "conclusions": doc.context.get("conclusions"),  # Added conclusions
                "relationships": doc.relationships
            }
            
            # Filter key points based on focus areas
            if focus_areas:
                filtered_points = []
                for point in info["key_points"]:
                    point_lower = point.lower()
                    if any(any(keyword in point_lower for keyword in focus_mapping[focus]) 
                          for focus in focus_areas):
                        filtered_points.append(point)
                info["key_points"] = filtered_points
            
            relevant_info.append(info)
            
        return relevant_info

    async def _integrate_information(
        self,
        relevant_info: List[Dict[str, Any]],
        original_query: str = None
    ) -> Dict[str, Any]:
        """Integrate information from multiple sources"""
        if not relevant_info:
            return {"main_points": [], "domains": set(), "summaries": [], "conclusions": []}
            
        integrated = {
            "main_points": [],
            "domains": set(),
            "summaries": [],
            "conclusions": [],  # Added conclusions
            "focus": self._determine_focus(original_query) if original_query else "general"
        }
        
        for info in relevant_info:
            # Add domain
            if info.get("domain"):
                integrated["domains"].add(info["domain"])
                
            # Add summary if available
            if info.get("summary"):
                integrated["summaries"].append(info["summary"])
                
            # Add key points
            integrated["main_points"].extend(info.get("key_points", []))
            
            # Add conclusions if available
            if info.get("conclusions"):
                integrated["conclusions"].append(info["conclusions"])
            
        # Remove duplicates while preserving order
        integrated["main_points"] = list(dict.fromkeys(integrated["main_points"]))
        integrated["summaries"] = list(dict.fromkeys(integrated["summaries"]))
        integrated["conclusions"] = list(dict.fromkeys(integrated["conclusions"]))
            
        return integrated

    def _determine_focus(self, query: str) -> str:
        """Determine the main focus of the query"""
        if not query:
            return "general"
            
        query_lower = query.lower()
        focus_mapping = {
            "temperature": ["temperature", "warming", "heat"],
            "biodiversity": ["biodiversity", "species", "ecosystem"],
            "coral": ["coral", "reef"],
            "ocean": ["ocean", "sea", "marine"],
            "conclusions": ["conclusion", "summary", "findings", "key"]
        }
        
        for focus, keywords in focus_mapping.items():
            if any(keyword in query_lower for keyword in keywords):
                return focus
        return "general"

    async def _generate_response(
        self,
        integrated_info: Dict[str, Any],
        intents: List[str],
        original_query: str = None
    ) -> str:
        """Generate response based on integrated information"""
        response_parts = []
        
        # Add domain context if available
        domains = integrated_info.get("domains", set())
        if domains:
            response_parts.append(f"Based on analysis of {', '.join(domains)} research:")
        
        # Determine focus and structure response accordingly
        focus = integrated_info.get("focus", "general")
        main_points = integrated_info.get("main_points", [])
        conclusions = integrated_info.get("conclusions", [])
        
        if focus == "temperature":
            temp_points = [p for p in main_points if any(k in p.lower() for k in ["temperature", "warming", "heat"])]
            if temp_points:
                response_parts.append("\nTemperature-related findings:")
                response_parts.extend(f"- {point}" for point in temp_points)
                
        elif focus == "biodiversity":
            bio_points = [p for p in main_points if any(k in p.lower() for k in ["biodiversity", "species", "ecosystem"])]
            if bio_points:
                response_parts.append("\nBiodiversity impacts:")
                response_parts.extend(f"- {point}" for point in bio_points)
                
        elif focus == "coral":
            coral_points = [p for p in main_points if any(k in p.lower() for k in ["coral", "reef"])]
            if coral_points:
                response_parts.append("\nCoral reef impacts:")
                response_parts.extend(f"- {point}" for point in coral_points)
                
        elif focus == "conclusions":
            response_parts.append("\nKey conclusions:")
            if conclusions:
                response_parts.extend(f"- {conclusion}" for conclusion in conclusions)
            else:
                response_parts.extend(f"- {point}" for point in main_points)
            
        else:  # general or other focus
            if main_points:
                response_parts.append("\nKey findings:")
                response_parts.extend(f"- {point}" for point in main_points)
        
        # If no structured information available
        if len(response_parts) <= 1:  # Only has domain intro
            response_parts.append("No relevant information found for this specific query.")
        
        return "\n".join(response_parts)

    def _calculate_confidence(
        self,
        documents: List[DocAnalysis],
        query: QueryAnalysis
    ) -> float:
        """Calculate confidence in synthesis result"""
        if not documents:
            return 0.0
            
        # Base confidence from query analysis
        confidence = query.confidence
        
        # Adjust based on number of relevant documents
        doc_factor = min(len(documents) / len(query.domains), 1.0) if query.domains else 0.5
        
        # Adjust based on content quality
        content_scores = []
        for doc in documents:
            score = 0.0
            if isinstance(doc.content, str) and doc.content.strip():
                score += 0.4  # Has non-empty content
            if doc.context.get("summary"):
                score += 0.3  # Has summary
            if doc.relationships:
                score += 0.3  # Has relationships
            content_scores.append(score)
            
        content_factor = sum(content_scores) / len(content_scores) if content_scores else 0.0
        
        return confidence * doc_factor * content_factor
