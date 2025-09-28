import json
import pandas as pd
from difflib import get_close_matches
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print(OPENROUTER_API_KEY)

# Carga procesos desde Process.txt
with open("Process.txt", "r", encoding="utf-8") as f:
    PROCESSES = [line.strip() for line in f.readlines() if line.strip()]


def shortlist_candidates(item, topn=20):
    """Devuelve los top-N procesos más parecidos a item."""
    matches = get_close_matches(item.lower(), [p.lower() for p in PROCESSES],
                                n=topn, cutoff=0.0)
    lower_to_orig = {p.lower(): p for p in PROCESSES}
    return [lower_to_orig[m] for m in matches if m in lower_to_orig]


def build_prompt(items, topn=20):
    prompt = {
        "idemat_candidates": [],
        "items": items
    }
    # Juntamos todos los candidatos para ahorrar tokens
    all_cands = {}
    for it in items:
        for c in shortlist_candidates(it, topn=topn):
            all_cands[c] = True
    prompt["idemat_candidates"] = [{"process": p} for p in list(all_cands.keys())]
    return prompt


SYSTEM_PROMPT = (
    "Eres un asistente experto que mapea descripciones de actividades de inventarios de GEI "
    "a el campo `process` de Idemat2025. Responde SOLO con un JSON que tenga el mismo "
    "número de elementos que la entrada, cada uno con `input` y `matched_process` "
    "(idéntico a la cadena del dataset). SIEMPRE encuentra el mejor match disponible - "
    "nunca uses null, siempre elige el proceso más apropiado de los candidatos disponibles."
)


def call_llm(system_prompt, user_payload):
    load_dotenv()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    """
    Llama a Grok 4 Fast via OpenRouter para mapear items a procesos Idemat2025.
    Debe devolver lista de dicts con {"input": ..., "matched_process": ...}
    """
    # Configuración del cliente OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    # Construir el prompt del usuario
    user_message = f"""
Items a mapear: {json.dumps(user_payload['items'], ensure_ascii=False, indent=2)}

Candidatos Idemat2025 disponibles: {json.dumps(user_payload['idemat_candidates'], ensure_ascii=False, indent=2)}

Por favor, mapea cada item a su proceso más similar en Idemat2025. Responde SOLO con un JSON válido.
"""

    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,  # Temperatura moderada para mejor creatividad
            max_tokens=2000
        )

        response_content = completion.choices[0].message.content

        # Intentar parsear la respuesta JSON
        try:
            result = json.loads(response_content)
            return result
        except json.JSONDecodeError:
            # Si no es JSON válido, intentar extraer JSON del texto
            import re
            json_match = re.search(r'\[.*\]', response_content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("No se pudo extraer JSON válido de la respuesta")

    except Exception as e:
        print(f"Error en la llamada a la API: {e}")
        # Devolver resultado por defecto con el mejor candidato disponible
        fallback_results = []
        for item in user_payload['items']:
            # Buscar el mejor candidato como fallback
            candidates = shortlist_candidates(item, topn=1)
            best_match = candidates[0] if candidates else "Electricity General Industry"
            fallback_results.append({
                "input": item,
                "matched_process": best_match,
                "source": "fallback"
            })
        return fallback_results


def map_items_to_idemat(items, topn=20):
    print("with ai")
    payload = build_prompt(items, topn=topn)
    return call_llm(SYSTEM_PROMPT, payload)


# === Cargar items desde CSV ===
def load_items_from_csv(csv_file):
    """Carga los items (issues) desde el archivo CSV"""
    try:
        df = pd.read_csv(csv_file)


        return df
    except Exception as e:
        print(f"⚠️ Error cargando CSV: {e}")
        # Fallback a ejemplos si no se puede cargar el CSV