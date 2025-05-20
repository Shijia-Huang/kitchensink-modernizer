import os
import argparse
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

def insert_suffix(filename, suffix):
    base, ext = os.path.splitext(filename)
    return f"{base}{suffix}{ext}"

def generate_prompt(code, mode="comment"):
    if mode == "modernize":
        return (
            "You are an expert software architect. Rewrite the following Java code to use modern best practices and frameworks "
            "(e.g., replace EJB with Spring Boot annotations, use dependency injection, REST APIs, etc.). "
            "Include inline comments that explain what each section does. Return the rewritten code with comments, no markdown formatting.\n\n"
            "Code:\n" + code
        )
    else:
        return (
            "You are an expert Java developer and code modernization assistant. "
            "I will provide you a Java source file. For each line of the code, "
            "add an inline comment using `//` that explains what the line does. "
            "If a line uses outdated or deprecated practices, include a modernization suggestion. "
            "Output the code with comments in plain text, without markdown formatting.\n\n"
            "Code:\n" + code
        )

def analyze_code(input_path, output_path, mode="comment"):
    with open(input_path, "r") as f:
        code = f.read()

    prompt_text = generate_prompt(code, mode)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt_text
        )
        result = response.text
    except Exception as e:
        print(f"Error while calling Gemini API: {e}")
        return

    with open(output_path, "w") as f:
        f.write(result)
    print(f"Annotated code saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Annotate or modernize Java code using Google Gemini")
    parser.add_argument("input_file", help="Path to the Java source file to analyze")
    parser.add_argument("-o", "--output", help="Optional output path for the generated file")
    parser.add_argument("-m", "--mode", choices=["comment", "modernize"], default="comment",
                        help="Choose 'comment' to add inline comments or 'modernize' to refactor to modern frameworks")

    args = parser.parse_args()
    output_file = args.output or insert_suffix(args.input_file, f"_{args.mode}ed")
    analyze_code(args.input_file, output_file, args.mode)

if __name__ == "__main__":
    main()
