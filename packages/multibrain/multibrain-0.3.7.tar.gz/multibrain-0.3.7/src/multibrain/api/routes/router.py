# src/multibrain/api/routes/router.py

import logging
from fastapi import APIRouter, Request
from pydantic import BaseModel
from ollama import AsyncClient
import asyncio
import toml

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

router = APIRouter()

# Load configuration from config.toml
with open("config.toml", "r") as f:
    config = toml.load(f)


class QueryRequest(BaseModel):
    query: str


async def get_response_from_ollama(host, model_name, query_request, source_name, color):
    logger = logging.getLogger(__name__)
    ollama_client = AsyncClient(host=host)

    try:
        message = {"role": "user", "content": query_request.query}
        response = await ollama_client.chat(
            model=model_name, messages=[message], stream=False
        )

        content = (
            response.message.content
            if hasattr(response, "message") and hasattr(response.message, "content")
            else str(response)
        )

        logger.debug(f"Extracted content from {host}: {content}")
        return {
            "response": content,
            "source": source_name,
            "model": model_name,
            "host": host,
            "color": color,
        }
    except Exception as e:
        logger.error(f"Error processing request for {host}: {e}")
        return {"error": str(e), "source": source_name, "host": host}


@router.post("/query")
async def run_query(query_request: QueryRequest, request: Request):
    logger = logging.getLogger(__name__)
    logger.debug(f"Received request: {query_request}")

    tasks = []
    for idx, server in enumerate(config["response_servers"][:16]):
        tasks.append(
            get_response_from_ollama(
                server["host"],
                server["model"],
                query_request,
                f"server{idx + 1}",
                server.get("color", "default-box"),
            )
        )

    responses = await asyncio.gather(*tasks)

    formatted_responses = []
    for response in responses:
        if "error" in response:
            formatted_responses.append(
                {
                    "response": f"<strong>Error:</strong> {response['error']}",
                    "source": response["source"],
                    "model": response.get("model", "Unknown"),
                    "host": response["host"],
                    "color": response.get("color", "default-box"),
                }
            )
        else:
            formatted_responses.append(
                {
                    "response": response["response"],
                    "source": response["source"],
                    "model": response["model"],
                    "host": response["host"],
                    "color": response.get("color", "default-box"),
                }
            )

    if len(formatted_responses) > 0:
        summary_query = f""" Task: Generate a concise, accurate summary by cross-referencing the following responses.
        Correct any discrepancies, remove hallucinations, and ensure factual integrity.

        Original Query:
        {query_request.query}

        Source Responses:"""
        for idx, resp in enumerate(formatted_responses):
            summary_query += (
                f"\n{idx + 1}. Response from {resp['source']}:\n{resp['response']}\n"
            )

        summary_query += """\nRequirements:
        - Prioritize factual consistency between sources.
        - Resolve conflicting information.
        - Eliminate redundant or fabricated content.
        - Ensure the summary reflects only validated information.
        - Remove hallucinations.
        - Don't note incorrect information, just omit it.
        - Don't mention information was removed or discrepancies, just omit it.
        - Write "Summary:\n" then write the summary.
        """

        summary_task = get_response_from_ollama(
            config["servers"]["summary_server_host"],
            config["models"]["summary_server"],
            QueryRequest(query=summary_query),
            "Summary Server",
            config.get("servers", {}).get("summary_server_color", "default-box"),
        )

        summary_response = await summary_task

        if "error" in summary_response:
            formatted_responses.append(
                {
                    "response": f"<strong>Error:</strong> {summary_response['error']}",
                    "source": summary_response["source"],
                    "model": summary_response.get("model", "Unknown"),
                    "host": summary_response["host"],
                    "color": summary_response.get("color", "default-box"),
                }
            )
        else:
            formatted_responses.append(
                {
                    "response": summary_response["response"],
                    "source": summary_response["source"],
                    "model": summary_response["model"],
                    "host": summary_response["host"],
                    "color": summary_response.get("color", "default-box"),
                }
            )

    logger.debug(f"Formatted responses: {formatted_responses}")

    return {"responses": formatted_responses}
