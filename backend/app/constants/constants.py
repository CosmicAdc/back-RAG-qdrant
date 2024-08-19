
import os

VLLM_MODEL: str = os.getenv("VLLM_MODEL", "Sreenington/Phi-3-mini-4k-instruct-AWQ")
VLLM_REMOTE_HOST: str = os.getenv("VLLM_REMOTE_HOST", "http://190.15.142.60:80")
VLLM_API_KEY: str = os.getenv("VLLM_API_KEY", "token-server-ai-vllm")
VLLM_MAX_TOKENS: int = int(os.getenv("VLLM_MAX_TOKENS", "2500"))

SEARCH_TYPE:str = os.getenv("SEARCH_TYPE", "mmr")


SEARCH_KWARGS: dict = {
    "k": int(os.getenv("k", "3")),
    "fetch_k": int(os.getenv("fetch_k", "5")),
    "lambda_mult": float(os.getenv("lambda_mult", "0.6"))
}

PREFIX = "fastapi"