from typing import Any
from aimon import Client                                        
from .aimon_evaluator import AIMonEvaluator, generate_random_string

class ContextRelevanceEvaluator(AIMonEvaluator):
    
    def __init__(self, 
                 aimon_client:Client, 
                 publish: bool = False, 
                 application_name:str = "ApplicationName"+generate_random_string(5), 
                 model_name:str = "ModelName"+generate_random_string(5)) -> None:                  
        
        super().__init__(aimon_client, publish, application_name, model_name)

    def create_payload(self, context, user_query, generated_text, task_definition) -> dict:
        
        aimon_payload = super().create_payload(context, 
                                               user_query, 
                                               user_instructions=None, 
                                               generated_text=generated_text, 
                                               config={'retrieval_relevance': {'detector_name': 'default'}}, task_definition = task_definition)
                
        return aimon_payload
    
    def evaluate(self, user_query, llamaindex_llm_response, task_definition, **kwargs: Any):

        context, response = self.extract_response_metadata(llamaindex_llm_response)

        aimon_payload = self.create_payload(context, user_query, response, task_definition)
    
        detect_response = self.detect_aimon_response(aimon_payload)

        ## Normalizing relevance scores for the ContextRelevanceEvaluator
        for item in detect_response.retrieval_relevance:
            if "relevance_scores" in item:
                item["relevance_scores"] = [score / 100 for score in item["relevance_scores"]]

        return detect_response.retrieval_relevance