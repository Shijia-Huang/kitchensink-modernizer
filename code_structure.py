import os
import argparse
import javalang

def extract_structure(java_file):
    with open(java_file, 'r') as file:
        source = file.read()

    try:
        tree = javalang.parse.parse(source)
        structure = []

        for type in tree.types:
            if isinstance(type, javalang.tree.ClassDeclaration):
                structure.append(f"## Class: {type.name}\n")
                if type.fields:
                    structure.append("### Fields:")
                    for field in type.fields:
                        field_type = field.type.name if hasattr(field.type, 'name') else str(field.type)
                        for declarator in field.declarators:
                            structure.append(f"- {field_type} {declarator.name}")
                if type.methods:
                    structure.append("\n### Methods:")
                    for method in type.methods:
                        params = ", ".join([f"{p.type.name} {p.name}" for p in method.parameters])
                        structure.append(f"- {method.name}({params})")

                structure.append("\n")
        return "\n".join(structure)

    except Exception as e:
        return f"Failed to parse {java_file}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Extract Java class and method structure into Markdown")
    parser.add_argument("java_file", help="Path to the Java source file")
    parser.add_argument("-o", "--output", help="Optional output Markdown file")
    args = parser.parse_args()

    output = extract_structure(args.java_file)

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Structure saved to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
