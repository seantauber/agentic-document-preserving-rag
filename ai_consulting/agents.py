from crewai import Agent
from textwrap import dedent

class ConsultingAgents:
    def __init__(self):
        self.document_analyzer = Agent(
            role='Document Analyzer',
            goal='Thoroughly analyze client documents to extract key business information and opportunities',
            backstory=dedent("""You are an expert at analyzing business documents and extracting 
            key insights about companies, their challenges, and opportunities for AI implementation."""),
            verbose=True,
            allow_delegation=False
        )
        
        self.ai_strategist = Agent(
            role='AI Strategy Expert',
            goal='Develop strategic AI implementation recommendations based on client analysis',
            backstory=dedent("""You are an expert AI strategist who can identify the best opportunities
            for AI implementation and develop detailed recommendations."""),
            verbose=True,
            allow_delegation=False
        )
        
        self.proposal_writer = Agent(
            role='Proposal Writer',
            goal='Create compelling and detailed consulting proposals',
            backstory=dedent("""You are an experienced proposal writer who knows how to create
            persuasive and professional consulting proposals that win clients."""),
            verbose=True,
            allow_delegation=False
        )
