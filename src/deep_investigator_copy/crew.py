import os


from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	FirecrawlSearchTool,
	FirecrawlScrapeWebsiteTool,
	FirecrawlCrawlWebsiteTool
)
from deep_investigator_copy.tools.evidence_log_tool import EvidenceLogTool
from deep_investigator_copy.tools.openbullet_mcp_tool import OpenBulletMCPTool






@CrewBase
class DeepInvestigatorCopyCrew:
    """DeepInvestigatorCopy crew"""

    
    @agent
    def floor_1_investigative_researcher(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_1_investigative_researcher"],
            
            
            tools=[
                FirecrawlSearchTool(),
                FirecrawlScrapeWebsiteTool(),
                FirecrawlCrawlWebsiteTool(),
                EvidenceLogTool(),
                OpenBulletMCPTool(),
            ],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_1_investigative_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_1_investigative_analyst"],
            
            
            tools=[EvidenceLogTool(), OpenBulletMCPTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_2_investigative_researcher(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_2_investigative_researcher"],
            
            
            tools=[
                FirecrawlSearchTool(),
                FirecrawlScrapeWebsiteTool(),
                FirecrawlCrawlWebsiteTool(),
                EvidenceLogTool(),
                OpenBulletMCPTool(),
            ],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_2_investigative_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_2_investigative_analyst"],
            
            
            tools=[EvidenceLogTool(), OpenBulletMCPTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_3_investigative_researcher(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_3_investigative_researcher"],
            
            
            tools=[
                FirecrawlSearchTool(),
                FirecrawlScrapeWebsiteTool(),
                FirecrawlCrawlWebsiteTool(),
                EvidenceLogTool(),
                OpenBulletMCPTool(),
            ],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_3_investigative_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_3_investigative_analyst"],
            
            
            tools=[EvidenceLogTool(), OpenBulletMCPTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_4_investigative_researcher(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_4_investigative_researcher"],
            
            
            tools=[
                FirecrawlSearchTool(),
                FirecrawlScrapeWebsiteTool(),
                FirecrawlCrawlWebsiteTool(),
                EvidenceLogTool(),
                OpenBulletMCPTool(),
            ],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_4_investigative_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_4_investigative_analyst"],
            
            
            tools=[EvidenceLogTool(), OpenBulletMCPTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_5_investigative_researcher(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_5_investigative_researcher"],
            
            
            tools=[
                FirecrawlSearchTool(),
                FirecrawlScrapeWebsiteTool(),
                FirecrawlCrawlWebsiteTool(),
                EvidenceLogTool(),
                OpenBulletMCPTool(),
            ],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_5_investigative_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_5_investigative_analyst"],
            
            
            tools=[EvidenceLogTool(), OpenBulletMCPTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_6_investigative_researcher(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_6_investigative_researcher"],
            
            
            tools=[
                FirecrawlSearchTool(),
                FirecrawlScrapeWebsiteTool(),
                FirecrawlCrawlWebsiteTool(),
                EvidenceLogTool(),
                OpenBulletMCPTool(),
            ],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    @agent
    def floor_6_investigative_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["floor_6_investigative_analyst"],
            
            
            tools=[EvidenceLogTool(), OpenBulletMCPTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
            
        )
        
    
    

    
    @task
    def floor_1_research(self) -> Task:
        return Task(
            config=self.tasks_config["floor_1_research"],
            markdown=False,
            
            
        )
    
    @task
    def floor_1_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["floor_1_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def floor_2_research(self) -> Task:
        return Task(
            config=self.tasks_config["floor_2_research"],
            markdown=False,
            
            
        )
    
    @task
    def floor_2_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["floor_2_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def floor_3_research(self) -> Task:
        return Task(
            config=self.tasks_config["floor_3_research"],
            markdown=False,
            
            
        )
    
    @task
    def floor_3_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["floor_3_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def floor_4_research(self) -> Task:
        return Task(
            config=self.tasks_config["floor_4_research"],
            markdown=False,
            
            
        )
    
    @task
    def floor_4_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["floor_4_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def floor_5_research(self) -> Task:
        return Task(
            config=self.tasks_config["floor_5_research"],
            markdown=False,
            
            
        )
    
    @task
    def floor_5_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["floor_5_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def floor_6_research(self) -> Task:
        return Task(
            config=self.tasks_config["floor_6_research"],
            markdown=False,
            
            
        )
    
    @task
    def floor_6_final_evidence_dump(self) -> Task:
        return Task(
            config=self.tasks_config["floor_6_final_evidence_dump"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the DeepInvestigatorCopy crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/deepseek-ai/DeepSeek-V3.1"),
        )

