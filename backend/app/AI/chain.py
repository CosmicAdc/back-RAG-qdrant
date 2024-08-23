from app.models.models import VLLM
from app.AI import PROMPTS
from langchain_core.output_parsers import StrOutputParser

def show(inputs):
    print(inputs)
    return inputs

base_chain_esp= PROMPTS.qa_prompt_spanish |show | VLLM
base_chain_en= PROMPTS.qa_prompt_english |show|VLLM 
