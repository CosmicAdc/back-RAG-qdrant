import httpx 

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.runnables import ConfigurableField
from langchain_community.llms import VLLMOpenAI
from app.constants import constants as settings
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.document_compressors import FlashrankRerank

    
http_client = httpx.Client(verify=False)

VLLM = VLLMOpenAI(
    openai_api_key=settings.VLLM_API_KEY,
    openai_api_base=f"{settings.VLLM_REMOTE_HOST}/v1",
    model_name=settings.VLLM_MODEL,
    max_tokens=settings.VLLM_MAX_TOKENS,
    temperature=0.1,
    model_kwargs={"stop": ["<|end|>","Human"]},
    http_client=http_client,
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

compressor = FlashrankRerank(top_n=3,model="ms-marco-MultiBERT-L-12")

model_name = "jinaai/jina-embeddings-v2-base-es"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


