from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from llm1 import LLMClient
from graph import run_cypher
from dataproduct_schema import GRAPH_SCHEMA
from cypher_queries import CYPHER_EXAMPLES
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.generation import GraphRAG
import nest_asyncio
import asyncio
import traceback

app = FastAPI()

class AskRequest(BaseModel):
    question: str

# Initialize LLM, retriever, and RAG pipeline at startup
my_LLMClient = LLMClient(api_key="<< LLM API key >>")
nest_asyncio.apply()
asyncio.run(LLMClient._get_session(my_LLMClient))
driver = None
retriever = None
rag = None

def get_rag():
    global driver, retriever, rag
    if rag is not None:
        return rag
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("<<user-name>>", "<<password>>")
    )
    retriever = Text2CypherRetriever(
        driver=driver,
        llm=my_LLMClient,
        neo4j_schema=GRAPH_SCHEMA,
        examples=CYPHER_EXAMPLES
    )
    rag = GraphRAG(retriever=retriever, llm=my_LLMClient)
    return rag

def extract_cypher_query(response: str) -> str:
    import re
    response = re.sub(r'`+', '', response)
    response = response.strip()
    cypher_keywords = (
        "MATCH", "RETURN", "WITH", "WHERE", "CREATE", "MERGE", "OPTIONAL", "UNWIND",
        "CALL", "SET", "DELETE", "DETACH", "ORDER", "SKIP", "LIMIT", "REMOVE",
        "FOREACH", "LOAD", "USING", "UNION"
    )
    lines = response.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().upper().startswith(cypher_keywords):
            start_idx = i
            break
    if start_idx is not None:
        cypher_lines = []
        for line in lines[start_idx:]:
            stripped = line.strip()
            if not stripped:
                break
            if (stripped.upper().startswith(cypher_keywords) or line.startswith("    ") or line.startswith("\t")):
                cypher_lines.append(line)
            else:
                break
        cypher = "\n".join(cypher_lines).strip()
        cypher = cypher.rstrip(';').strip()
        cypher = re.sub(r'`+', '', cypher).strip()
        return cypher
    for line in lines:
        if line.strip().upper().startswith(cypher_keywords):
            return re.sub(r'`+', '', line.strip())
    return re.sub(r'`+', '', response.strip())

@app.post("/ask")
async def ask_endpoint(req: AskRequest):
    try:
        rag = get_rag()
        response = rag.search(query_text=req.question)
        cypher = extract_cypher_query(response.generated_query)
        try:
            results = run_cypher(cypher)
        except Exception as e:
            results = None
        return {
            "cypher": cypher,
            "answer": getattr(response, "answer", None),
            "results": results
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()}) 
