import json

def process_gemini_response(gemini_response):
    try:
        # Remove ```json prefix and suffix
        gemini_response = gemini_response.strip('```json')
        # Convert JSON string to Python dictionary
        data_dict = json.loads(gemini_response)
        return data_dict
    except Exception as e:
        # If an error occurs, handle it accordingly
        print("An error occurred while processing the Gemini response:", e)
        raise ValueError("Invalid Gemini response")

# Example usage:
# gemini_response = '```json\n{"key": "value"}\n```'
# try:
#     result = process_gemini_response(gemini_response)
#     print("Result:", result)
# except ValueError as ve:
#     print(ve)
