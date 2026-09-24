from pydantic import BaseModel, Field
import httpx
from typing import AsyncGenerator


class Pipe:
    class Valves(BaseModel):
        LANGFLOW_API_KEY: str = Field(
            default="", description="Chave de API do Langflow"
        )
        LANGFLOW_URL: str = Field(
            default="http://langflow:7860", description="URL do Langflow"
        )
        FLOW_ID: str = Field(
            default="id do fluxo",
            description="ID do Fluxo no Langflow",
        )

    def __init__(self):
        self.valves = self.Valves()

    async def pipe(self, body: dict) -> AsyncGenerator[str, None]:
        # 1. Extrai a última mensagem enviada no chat
        messages = body.get("messages", [])
        if not messages:
            yield "Erro: Nenhuma mensagem no payload"
            return

        last_message = messages[-1].get("content", "")

        if isinstance(last_message, list):
            for item in last_message:
                if isinstance(item, dict) and item.get("type") == "text":
                    last_message = item.get("text", "")
                    break

        # 2. Ignora requisições automáticas do Open WebUI
        if "### Task:" in str(last_message):
            yield ""
            return

        # 3. Payload conforme especificação do Langflow
        payload = {
            "model": self.valves.FLOW_ID,
            "input": str(last_message),
            "stream": False,
        }

        headers = {
            "x-api-key": self.valves.LANGFLOW_API_KEY,
            "Content-Type": "application/json",
        }

        url = f"{self.valves.LANGFLOW_URL.rstrip('/')}/api/v1/responses"

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()

            data = response.json()

            # 4. Extração direta do texto puro de saída
            outputs = data.get("output", [])
            if outputs and len(outputs) > 0:
                content = outputs[0].get("content", [])
                if content and len(content) > 0:
                    text_response = content[0].get("text", "")
                    # Envia exatamente o texto retornado pelo fluxo ("Projeto 4.8 Req 7- MCP-Get no notion")
                    yield text_response
                    return

            yield "Nenhuma resposta encontrada"

        except Exception as e:
            yield f"Erro no processamento: {str(e)}"
