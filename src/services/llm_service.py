import yaml
from google import genai
from google.genai import types


class LLMService:
    def __init__(self, api_key: str, model_name: str, semantic_layer_path: str):
        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name
        with open(semantic_layer_path, "r", encoding="utf-8") as f:
            self._semantic_context = yaml.safe_load(f)

    @property
    def semantic_context(self) -> dict:
        return self._semantic_context

    def generate_sql(self, question: str) -> str:
        system_instruction = f"""
        You are a Senior Data Warehouse (DWH) Architect. Translate the user's natural language question into an accurate MariaDB SQL query.

        Use ONLY the provided semantic layer below and strictly enforce all 'business_rules':
        {yaml.dump(self._semantic_context, allow_unicode=True)}

        Rules:
        - Return ONLY raw SQL code without markdown formatting (no ```sql or ```).
        - The query must start with SELECT or WITH.
        """

        response = self._client.models.generate_content(
            model=self._model_name,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0,
            ),
        )
        return response.text.strip().replace("```sql", "").replace("```", "").strip()
