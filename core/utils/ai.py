from google import genai
from django.conf import settings


def prompt_gemini(prompt, model=None):
    if settings.GEMINI_API_KEY is None:
        raise Exception("Gemini api key not found")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    if model is None:
        try:
            model = settings.GEMINI_MODEL or "models/gemini-2.0-flash"
        except AttributeError:
            model = "models/gemini-2.0-flash"

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response
