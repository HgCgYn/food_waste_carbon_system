"""VLM (Vision Language Model) service for secondary food classification.

This service is called only when YOLO's confidence for a detected object
falls below the configured threshold. It crops the bounding box region
from the original image and sends it to either Gemini or OpenAI GPT
for a second-opinion classification.
"""

import base64
import io
import logging
import os

from PIL import Image

logger = logging.getLogger(__name__)

# NOTE: 可辨識的食物 YOLO 標籤清單，用於引導 VLM 從中選擇最接近的類別
FOOD_LABEL_LIST: list[str] = [
    "apple", "asparagus", "bacon", "baked potatoes", "banana", "beans",
    "black bean", "blueberries", "boiled egg", "bread", "breaded", "brocolis",
    "cabbage", "cabidela rice", "cake", "carrot", "cereals", "cheese",
    "chicken", "chicken steak", "chips", "chorizo", "coffee", "cucumber",
    "cutlet", "fish", "fish hake", "french fries", "fried cod", "fried egg",
    "gelatin", "grape", "greens", "grilled chop", "grilled steak", "ham",
    "lasagna", "lettuce", "lime", "mashed potatoes", "meatballs", "melon",
    "minced meat", "mushrooms", "mussel", "olives", "omelet", "onion",
    "pasta", "pineapple", "pizza", "pork", "pork belly", "pork intestines",
    "pork loin", "rice", "salmon", "scrambled eggs", "scrambled eggs with bacon",
    "soup", "spaghetti", "steak", "steaks with mushrooms", "stewed veal",
    "strawberry", "toasted bread", "tomato", "tuna", "tuna with mushrooms",
    "tuna with pasta", "turkey steak", "vegetables", "watermelon",
]

# NOTE: VLM 回傳此值代表「非食物，應排除」
UNKNOWN_LABEL = "unknown"

_VLM_PROMPT_TEMPLATE = """You are a food classification assistant.

The image is a cropped region from a cafeteria food tray.
YOLO detected this region as "{yolo_label}" but with low confidence (below 70%).

Please identify the food item and select the MOST appropriate label from the
following list. If the item is NOT food (e.g. a napkin, utensil, or garbage),
reply with exactly: unknown

Available labels:
{label_list}

Reply with ONLY the label name from the list above, nothing else.
Do not add punctuation, explanation, or quotes."""


def _pil_to_base64_jpeg(image: Image.Image) -> str:
    """Convert a PIL Image to a base64-encoded JPEG string."""
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


class VLMService:
    """
    Wraps Gemini and OpenAI vision APIs for low-confidence object re-classification.

    Usage:
        service = VLMService(model="yolo_gemini")
        corrected = service.confirm_low_confidence_item(cropped_image, "bowl")
    """

    def __init__(self, model: str) -> None:
        """
        Args:
            model: One of "yolo_gemini" or "yolo_gpt".

        Raises:
            ValueError: If model is not a recognised VLM mode.
            EnvironmentError: If the required API key is not set.
        """
        if model not in ("yolo_gemini", "yolo_gpt"):
            raise ValueError(f"VLMService: unsupported model '{model}'")
        self.model = model
        self._validate_api_key()

    # ──────────────────────────────────────────────────────────────────────────
    # Public interface
    # ──────────────────────────────────────────────────────────────────────────

    def confirm_low_confidence_item(
        self,
        cropped_image: Image.Image,
        yolo_label: str,
    ) -> str:
        """Send a cropped bounding-box image to the configured VLM for re-classification.

        Args:
            cropped_image: PIL Image of the YOLO bounding box region.
            yolo_label: The original YOLO label (used in the prompt as context).

        Returns:
            A label string from FOOD_LABEL_LIST, or UNKNOWN_LABEL if the VLM
            determines the object is not food.
        """
        prompt = _VLM_PROMPT_TEMPLATE.format(
            yolo_label=yolo_label,
            label_list=", ".join(FOOD_LABEL_LIST),
        )
        image_b64 = _pil_to_base64_jpeg(cropped_image)

        if self.model == "yolo_gemini":
            return self._call_gemini(image_b64, prompt)
        return self._call_openai(image_b64, prompt)

    # ──────────────────────────────────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _validate_api_key(self) -> None:
        """Raise EnvironmentError early if the required API key is absent."""
        if self.model == "yolo_gemini":
            key = os.environ.get("GEMINI_API_KEY", "").strip()
            if not key:
                raise EnvironmentError(
                    "GEMINI_API_KEY is not set. Please add it to your .env file."
                )
        else:
            key = os.environ.get("OPENAI_API_KEY", "").strip()
            if not key:
                raise EnvironmentError(
                    "OPENAI_API_KEY is not set. Please add it to your .env file."
                )

    def _call_gemini(self, image_b64: str, prompt: str) -> str:
        """Call Google Gemini Vision API and return the normalised label."""
        try:
            import google.generativeai as genai  # type: ignore

            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-2.5-flash")

            # Build an inline image part from the base64 string
            image_part = {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_b64,
                }
            }
            response = model.generate_content([prompt, image_part])
            raw = response.text.strip().lower()
            return self._normalise_label(raw)

        except EnvironmentError:
            raise
        except Exception as exc:
            logger.error("Gemini API call failed: %s", exc)
            return UNKNOWN_LABEL

    def _call_openai(self, image_b64: str, prompt: str) -> str:
        """Call OpenAI GPT-4o Vision API and return the normalised label."""
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}",
                                    "detail": "low",
                                },
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
                max_tokens=20,
            )
            raw = response.choices[0].message.content.strip().lower()
            return self._normalise_label(raw)

        except EnvironmentError:
            raise
        except Exception as exc:
            logger.error("OpenAI API call failed: %s", exc)
            return UNKNOWN_LABEL

    @staticmethod
    def _normalise_label(raw: str) -> str:
        """Validate VLM output against the known label list.

        Returns the matched label from FOOD_LABEL_LIST, or UNKNOWN_LABEL if
        the response is not a known food item.
        """
        cleaned = raw.strip().lower().strip(".'\"")
        if cleaned == UNKNOWN_LABEL:
            return UNKNOWN_LABEL
            
        # 1. Exact match
        for label in FOOD_LABEL_LIST:
            if label.lower() == cleaned:
                return label
                
        # 2. Lenient match (e.g. 'tomato' in 'tomatoes', or 'grilled chicken' -> 'chicken')
        for label in FOOD_LABEL_LIST:
            if label.lower() in cleaned or cleaned in label.lower():
                return label
                
        # NOTE: Fallback — VLM 回傳了非清單內的內容，視為無法辨識
        logger.warning("VLM returned unrecognised label: '%s', treating as unknown", raw)
        return UNKNOWN_LABEL
