import os
from crewai import Crew
from dotenv import load_dotenv
from agents import ConsultingAgents
from tasks import ConsultingTasks

def main(docs_folder):
    # Load environment variables
    load_dotenv()
    
    # Initialize agents
    agents = ConsultingAgents()
    
    # Create tasks
    tasks = ConsultingTasks(agents)
    
    # Define the sequence of tasks
    task_list = [
        tasks.analyze_documents(docs_folder),
        tasks.develop_ai_strategy(),
        tasks.write_proposal()
    ]
    
    # Create and run the crew
    crew = Crew(
        agents=[
            agents.document_analyzer,
            agents.ai_strategist,
            agents.proposal_writer
        ],
        tasks=task_list,
        verbose=2
    )
    
    # Execute the tasks
    result = crew.kickoff()
    
    return result

if __name__ == "__main__":
    # Specify the folder containing client documents
    docs_folder = "client_docs"
    
    # Run the proposal generation process
    proposal = main(docs_folder)
    print("\nFinal Proposal:")
    print(proposal)
