from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.runnables import ConfigurableField
from langchain_community.llms import VLLMOpenAI
from app.constants import constants as settings

    
    
VLLM = VLLMOpenAI(
    openai_api_key=settings.VLLM_API_KEY,
    openai_api_base=f"{settings.VLLM_REMOTE_HOST}/v1",
    model_name=settings.VLLM_MODEL,
    max_tokens=settings.VLLM_MAX_TOKENS,
    temperature=0.1,
    model_kwargs={"stop": ["<|end|>","\n\n\n"]},
).configurable_fields(
    temperature=ConfigurableField(
        id="temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
    ),
    max_tokens=ConfigurableField(
        id="max_tokens",
        name="LLM Max New Tokens",
        description="The max new tokens of the LLM",
    ),
)

model_name = "jinaai/jina-embeddings-v2-base-es"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

