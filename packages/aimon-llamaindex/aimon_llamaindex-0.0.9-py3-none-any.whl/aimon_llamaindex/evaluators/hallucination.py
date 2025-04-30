from typing import Any                                              
from aimon import Client
from .aimon_evaluator import AIMonEvaluator, generate_random_string

class HallucinationEvaluator(AIMonEvaluator):
    
    def __init__(self, 
                 aimon_client:Client, 
                 publish: bool = False, 
                 application_name:str = "ApplicationName"+generate_random_string(5), 
                 model_name:str = "ModelName"+generate_random_string(5)) -> None:                  
        
        super().__init__(aimon_client, publish, application_name, model_name)

    def create_payload(self, context, user_query, generated_text):
        
        aimon_payload = super().create_payload(context, 
                                               user_query, 
                                               user_instructions=None, 
                                               generated_text=generated_text, 
                                               config={'hallucination': {'detector_name': 'default'}})

        return aimon_payload
    
    def evaluate(self, user_query, llamaindex_llm_response, **kwargs: Any):

        context, response = self.extract_response_metadata(llamaindex_llm_response)

        aimon_payload = self.create_payload(context, user_query, response)
    
        detect_response = self.detect_aimon_response(aimon_payload)

        return detect_response.hallucination
    