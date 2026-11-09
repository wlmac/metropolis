from django.conf import settings
from google import genai


def prompt_gemini(prompt, model=None):
    if settings.GEMINI_API_KEY is None:
        raise Exception("Gemini api key not found")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    if model is None:
        try:
            model = settings.GEMINI_MODEL or "models/gemini-flash-latest"
        except AttributeError:
            model = "models/gemini-flash-latest"

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response
