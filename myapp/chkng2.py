import google.generativeai as genai

# 🔑 Replace with your API key
genai.configure(api_key="AQ.Ab8RN6KMy_1JZTPYv2hPFN7cge8ESy2tq6QPZTsiV6BB0VQJDg")

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

from google.api_core import exceptions


def generate_image(image, type_name):
    # Mapping logic
    language_map = {
        "html": "modern HTML5 page with CSS",
        "java": "java code",
        "react": "react page code",
        "flutter": "flutter page code with designs"
    }

    language = language_map.get(type_name, "code")

    full_prompt = f"""
    Convert the following {image} image into a clean,{language} .
    Only return {type_name} code (no explanation).
    """

    try:
        response = model.generate_content(full_prompt)
        print(response,"response")
        return response.text
    except exceptions.ResourceExhausted:
        return "ERROR:LIMIT_REACHED"
    except exceptions.ServiceUnavailable:
        return "ERROR:SERVER_OVERLOAD"
    except Exception as e:
        print(f"Error: {e}")
        return "ERROR:GENERIC_FAIL"



# 📝 User input
# user_input = input("Enter your website description:\n")
#
# # Generate HTML
# html_code = generate_html(user_input)
#
# # Save to file
# with open("generated.html", "w", encoding="utf-8") as f:
#     f.write(html_code)
#
# print("✅ HTML file generated: generated.html")