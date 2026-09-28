import os
import subprocess
import json
import time


def generate_answer(prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set."
        )

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/interactions?key="
        + api_key
    )

    data = {
        "model": "gemini-3.6-flash",
        "input": prompt
    }

    json_data = json.dumps(data)

    max_retries = 4

    for attempt in range(max_retries):

        print(
            f"Gemini request attempt "
            f"{attempt + 1}/{max_retries}"
        )

        result = subprocess.run(
            [
                "curl",
                "--max-time",
                "120",
                "-s",
                "-X",
                "POST",
                url,
                "-H",
                "Content-Type: application/json",
                "-d",
                json_data
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"Request failed. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            raise RuntimeError(
                "Gemini request failed:\n"
                + result.stderr
            )

        try:
            response = json.loads(
                result.stdout
            )

        except json.JSONDecodeError:

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"Invalid response. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            raise RuntimeError(
                "Gemini returned an invalid response."
            )

        # -----------------------------
        # CHECK GEMINI ERROR
        # -----------------------------

        if "error" in response:

            error = response["error"]

            error_code = error.get(
                "code",
                "unknown"
            )

            error_message = error.get(
                "message",
                "Unknown Gemini error"
            )

            # Temporary server/capacity error
            if (
                error_code in [
                    "service_unavailable",
                    "api_error",
                    "too_many_requests"
                ]
                or "high demand" in error_message.lower()
            ):

                if attempt < max_retries - 1:

                    wait_time = 5 * (2 ** attempt)

                    print(
                        f"Gemini is temporarily busy."
                    )

                    print(
                        f"Retrying in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            # Permanent error
            raise RuntimeError(
                "Gemini API error: "
                + error_message
            )

        # -----------------------------
        # EXTRACT MODEL ANSWER
        # -----------------------------

        for step in response.get(
            "steps",
            []
        ):

            if step.get(
                "type"
            ) == "model_output":

                for content in step.get(
                    "content",
                    []
                ):

                    if content.get(
                        "type"
                    ) == "text":

                        return content.get(
                            "text"
                        )

        return "No answer was generated."

    return "Gemini could not generate an answer."