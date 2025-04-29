import re
import json
from typing import List, Dict, Any

import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

# from utils import setup_logger, read_yaml_file # to-do
from prompts import CLAIM_EXTRACTOR_PROMPT



# logger = setup_logger() # to-do
# config = read_yaml_file("settings/config.yaml") # to-do



class Safeguards:
    """A class to run RAG metrics
    
    ### Attributes:
        - model_name (str): LLM model name (currently only GPT models are avaiable)
        - api_key (str): LLM provider API Key
    
    ### Methods:
        - extract_claims: extract the claims/statements from a given text.
        - get_cosine_similarity: computes the cosine similarity for claims and context embeddings (used only when evaluation method is set to "cosine").
        - eval_factuality: evaluates the contextual relevancy for each claim given the context (used only when evaluation method is set to "llm").
        - faithfulness: runs faithfulness avaliation.
    """
    def __init__(
        self,
        model_name: str,
        api_key: str
    ) -> None: 
        self.model_name = model_name
        self.api_key = api_key

    def extract_claims(
        self, 
        text: str, 
        extraction_method: str
    ) -> List[str]:
        """Split a paragraph into claims.

        ### Args
            - text (str): text paragraph to be splitted by sentences (claims)
            - extraction_method (str): how the claims will be extracted (llm, regex)
        
        ### Returns:
            - (List[str]): a list of sentences (claims)

        ### Note:
            The Regex pattern aims to finds a whitespace that:
            - is preceded by a period, exclamation or interrogation
            - is not preceded by the pattern word.word.character
            - is not predece by abreviation like 'Dr.'
        """
        if extraction_method == "regex":
            ending_patterns = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
            claims = re.split(ending_patterns, text.strip())

            return claims
        
        if extraction_method == "llm":
            openai_client = OpenAI(api_key=self.api_key)
            llm_output = openai_client.responses.create(
                model=self.model_name,
                instructions=CLAIM_EXTRACTOR_PROMPT,
                input=text,
                temperature=0,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "claims_list",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "claims": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["claims"],
                            "additionalProperties": False
                        },
                        "strict": True
                    }
                }
            )
            claims = json.loads(llm_output.output_text)['claims']
            
            return claims
        
    # def get_cosine_similarity(
    #     self, 
    #     claims: List[str], 
    #     context: str
    # ) -> float:
    #     """Computes the cosine similarity for claims and context embeddings.

    #     ### Args
    #         claims (List[str]): extracted claims from the LLM response.
    #         context (str): retrived context used to support or refute the claims.
        
    #     ### Returns:
    #         (float): computed cosine similarity.
    #     """
    #     cos_sim = []
    #     claim_embeddings = embedding_model(claims)
    #     context_embeddings = embedding_model(context)
    #     for c in claim_embeddings:
    #         claim_array = np.array(c).reshape(1, -1)
    #         context_array = np.array(context_embeddings).reshape(1, -1)
    #         cos_sim.append(cosine_similarity(claim_array, context_array)[0][0])
        
    #     return cos_sim

    
    # def eval_factuality(
    #     self, 
    #     claims: List[str], 
    #     context: str
    # ) -> Dict[str, List[str]]:
    #     """Evaluates the contextual relevancy for each claim given the context.

    #     ### Args:
    #         claims (list): extracted claims to be evaluated.
    #         context (str): context used to support or refute the claims.

    #     ### Returns:
    #         (dict): context supported claims and non supported claims.
    #     """
    #     factuality_agent = GenerativeModel(
    #         model_name=config[4]["model"],
    #         system_instruction=FACTUALITY_EVALUATOR_PROMPT.format(
    #             context=context
    #         )
    #     )
    #     llm_output = factuality_agent.generate_content(
    #         contents="\n> ".join(claims),
    #         generation_config=GenerationConfig(
    #             temperature=config[4]["temperature"],
    #             response_mime_type=config[4]["response_format"]
    #         )
    #     )
    #     factuality = json.loads(llm_output.text)

    #     return factuality

    # def faithfulness(
    #     self, 
    #     response: str, 
    #     context: str,
    #     claim_ext_method: str = "llm",
    #     evaluation_method: str = "llm",
    #     threshold: float = 0.7
    # ) -> Dict[str, Any]:
    #     """Calculates the faithfulness score for the LLM response from a given context.

    #     ### Args:
    #         response (str): response to be evaluated.
    #         context (str): context used to support or refute the claims.
    #         claim_ext_method (str): the method used to extract claims from the response.
    #         evaluation_method (str): the method used to run the metric evaluation.
    #         threshold (float): the minimum cosine similarity score for a claim to be considered supported.
            
    #     ### Returns:
    #         (Dict[str, Any]): the faithfulness score (proportion of supported claims).
        
    #     ### Note:
    #         The faithfulness score goes from 0 (no claims supported by the context) to 1 (all claims supported by the context).
    #     """
    #     claims = self.extract_claims(response, claim_ext_method)

    #     if evaluation_method == "cosine":
    #         cos_sim_scores = self.get_cosine_similarity(claims, context)
    #         supported_claims_count = sum(1 for score in cos_sim_scores if score >= threshold)
    #         supported_claims = [claims[i].strip() for i in range(len(cos_sim_scores)) if cos_sim_scores[i] >= threshold]
    #         non_supported_claims = [claims[i].strip() for i in range(len(cos_sim_scores)) if cos_sim_scores[i] < threshold]   
    #         faithfulness_score = supported_claims_count / len(claims)
    #         logger.info(f"FAITHFULNESS SCORE: {faithfulness_score}.")
            
    #         return {"faithfulness_score": faithfulness_score, "claims":claims, "supported_claims":supported_claims, "non_supported_claims": non_supported_claims}

    #     if evaluation_method == "llm":
    #         eval_results = self.eval_factuality(claims, context)
    #         faithfulness_score = len(eval_results["supported_claims"]) / len(claims)
    #         logger.info(f"FAITHFULNESS SCORE: {faithfulness_score}.")

    #         return {"faithfulness_score": faithfulness_score, "claims":claims, "supported_claims":eval_results["supported_claims"], "non_supported_claims": eval_results["non_supported_claims"]}
