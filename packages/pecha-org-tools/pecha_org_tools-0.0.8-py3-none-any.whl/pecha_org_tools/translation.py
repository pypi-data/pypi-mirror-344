import os
from typing import Any, Dict

import anthropic


def get_claude_response(prompt: str):
    try:
        # Initialize the client with your API key
        ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        if not ANTHROPIC_API_KEY:
            raise ValueError("Please set ANTHROPIC_API_KEY environment variable")


        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Create a message request
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",  # Specify the model version
            max_tokens=1000,  # Set maximum tokens for the response
            temperature=0,  # Adjust randomness of responses (0.0 for deterministic)
            system="You are a helpful assistant.",  # System message for context
            messages=[{"role": "user", "content": prompt}],
        )

        # Print the response content
        return response.content[0].text
    except Exception as e:
        print(e)
        return "Error in getting response from Claude"


def translate_to_en(text: str):
    prompt = f"""You are a professional translator doing translation  to English language.

    Follow these strict guidelines:

    1. Translate the text with the highest linguistic accuracy
    2. Preserve the original meaning and nuanced context
    3. Use clear, natural English that sounds like a native speaker
    4. If the text contains cultural or idiomatic expressions, provide a culturally appropriate equivalent
    5. Avoid literal word-for-word translations
    6. Return ONLY the English translation, with no additional commentary or explanation

    Source Text:
    {text}

    Translation:"""

    response = get_claude_response(prompt)
    return response.strip()


def translate_to_bo(text: str):
    prompt = f"""You are a professional translator doing translation to Tibetan language.

    Follow these strict guidelines:

    1. Translate the text with the highest linguistic accuracy
    2. Preserve the original meaning and nuanced context
    3. Use clear, natural Tibetan that sounds like a native speaker
    4. If the text contains cultural or idiomatic expressions, provide a culturally appropriate equivalent
    5. Avoid literal word-for-word translations
    6. Return ONLY the Tibetan translation, with no additional commentary or explanation

    Source Text:
    {text}

    Translation:"""

    response = get_claude_response(prompt)
    return response.strip()


def get_en_content_translation(pecha_content: Dict[str, Any]):
    """
    Get the literal english translation of the content complex structure
    Eg: Input:> pecha_content = {
                "བོད་": {"data": ["བོད་ནི་འཛམ་གླིང་གི་ས་ཆ་མཐོ་ཤོས་དང་ཆེས་ངོམས་ཅན་གྱི་ས་ཁུལ་ཞིག་ཡིན།"],
                        "བོད་མི་": {"གཞི་གྲངས་": []},
                "སྨོན་ལམ་རིག་ནུས།་": {"data": [],"མཉེན་ཆས་སྒྱུར་ཞིབ་": {"data": []}}
                }

        Output:> en_content = {
            "Tibet":{"data":[], "Tibetans": {"data":[]},
            "Monlam AI": {"data":[],"Machine Translation": {"data":[]}}
        }

    1. The keys are translated, except for the "data" key which is same.
    2. The values of the "data" key in output should be empty list.
    """
    en_content: Dict[str, Any] = {}
    for key, value in pecha_content.items():
        if key == "data":
            en_content[key] = []
            continue

        en_key = translate_to_en(key)
        en_content[en_key] = get_en_content_translation(value)

    return en_content


def get_bo_content_translation(pecha_content: Dict[str, Any]):
    """
    Get the literal tibetan translation of the content complex structure
    Eg: Input:> pecha_content = {
            "Tibet":{"data":[], "Tibetans": {"data":[]},
            "Monlam AI": {"data":[],"Machine Translation": {"data":[]}}
        }

        Output:> bo_content = {
                "བོད་": {"data": ["བོད་ནི་འཛམ་གླིང་གི་ས་ཆ་མཐོ་ཤོས་དང་ཆེས་ངོམས་ཅན་གྱི་ས་ཁུལ་ཞིག་ཡིན།"],
                        "བོད་མི་": {"གཞི་གྲངས་": []},
                "སྨོན་ལམ་རིག་ནུས།་": {"data": [],"མཉེན་ཆས་སྒྱུར་ཞིབ་": {"data": []}}
        }
    1. The keys are translated, except for the "data" key which is same.
    2. The values of the "data" key in output should be empty list.
    """
    en_content: Dict[str, Any] = {}
    for key, value in pecha_content.items():
        if key == "data":
            en_content[key] = []
            continue

        en_key = translate_to_bo(key)
        en_content[en_key] = get_bo_content_translation(value)

    return en_content
