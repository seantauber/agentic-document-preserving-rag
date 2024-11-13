from crewai import Task
from textwrap import dedent

class ConsultingTasks:
    def __init__(self, agents):
        self.agents = agents
    
    def analyze_documents(self, docs_folder):
        return Task(
            description=dedent(f"""
                Analyze all documents in the {docs_folder} folder.
                Extract key information about:
                1. Client's business model and operations
                2. Current challenges and pain points
                3. Technology infrastructure
                4. Industry context and competition
                
                Create a comprehensive analysis report.
            """),
            agent=self.agents.document_analyzer
        )

    def develop_ai_strategy(self):
        return Task(
            description=dedent("""
                Based on the document analysis, develop an AI implementation strategy:
                1. Identify top 3-5 opportunities for AI implementation
                2. Evaluate feasibility and potential impact
                3. Outline required resources and timeline
                4. Estimate potential ROI
                
                Create a strategic recommendations document.
            """),
            agent=self.agents.ai_strategist
        )

    def write_proposal(self):
        return Task(
            description=dedent("""
                Create a professional consulting proposal including:
                1. Executive Summary
                2. Situation Analysis
                3. Proposed AI Solutions
                4. Implementation Plan
                5. Timeline and Milestones
                6. Budget and ROI Projections
                7. About Our Team
                
                Format as a polished, client-ready proposal document.
            """),
            agent=self.agents.proposal_writer
        )
