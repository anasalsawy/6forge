from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class TheSixStageForgeCrew:
    """TheSixStageForge crew"""

    
    @agent
    def first_stage_work_enhancer_and_fixer(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["first_stage_work_enhancer_and_fixer"],
            
            
            tools=[],
            
            reasoning=True,
            max_reasoning_attempts=1,
            inject_date=True,
            allow_delegation=False,
            max_iter=1,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
        )
        
    
    @agent
    def second_stage_work_enhancer_and_fixer(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["second_stage_work_enhancer_and_fixer"],
            
            
            tools=[],
            
            reasoning=True,
            max_reasoning_attempts=2,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
        )
        
    
    @agent
    def third_stage_work_enhancer_and_fixer(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["third_stage_work_enhancer_and_fixer"],
            
            
            tools=[],
            
            reasoning=True,
            max_reasoning_attempts=3,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
        )
        
    
    @agent
    def fourth_stage_work_enhancer_and_fixer(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["fourth_stage_work_enhancer_and_fixer"],
            
            
            tools=[],
            
            reasoning=True,
            max_reasoning_attempts=3,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
        )
        
    
    @agent
    def fifth_stage_work_enhancer_and_fixer(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["fifth_stage_work_enhancer_and_fixer"],
            
            
            tools=[],
            
            reasoning=True,
            max_reasoning_attempts=3,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
        )
        
    
    @agent
    def sixth_stage_final_enhancer_and_delivery_agent(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["sixth_stage_final_enhancer_and_delivery_agent"],
            
            
            tools=[],
            
            reasoning=True,
            max_reasoning_attempts=3,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/deepseek-ai/DeepSeek-V3.1",
                
                
            ),
        )
        
    

    
    @task
    def stage_1_refinement(self) -> Task:
        return Task(
            config=self.tasks_config["stage_1_refinement"],
            markdown=False,
            
        )
    
    @task
    def stage_2_refinement(self) -> Task:
        return Task(
            config=self.tasks_config["stage_2_refinement"],
            markdown=False,
            
            
        )
    
    @task
    def stage_3_refinement(self) -> Task:
        return Task(
            config=self.tasks_config["stage_3_refinement"],
            markdown=False,
            
            
        )
    
    @task
    def stage_4_refinement(self) -> Task:
        return Task(
            config=self.tasks_config["stage_4_refinement"],
            markdown=False,
            
            
        )
    
    @task
    def stage_5_refinement(self) -> Task:
        return Task(
            config=self.tasks_config["stage_5_refinement"],
            markdown=False,
            
            
        )
    
    @task
    def stage_6_final_output(self) -> Task:
        return Task(
            config=self.tasks_config["stage_6_final_output"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the TheSixStageForge crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )

