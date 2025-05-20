import os

OLD_ANNOTATIONS = {
    '@Stateless': '🔴 Found @Stateless (EJB). Suggest replacing with Spring @Service.',
    '@Entity': '🟡 Found @Entity. Ensure use of modern ORM practices (Spring Data JPA).',
}

XML_WARNINGS = {
    'web.xml': '🔴 Found web.xml (legacy servlet config). Consider replacing with @WebServlet or Spring Boot.',
    'beans.xml': '🟡 Found beans.xml (CDI config). May not be needed in Spring.',
    '-ds.xml': '🔴 Found deprecated -ds.xml datasource config. Use application.properties or YAML.',
}

def scan_java_file(file_path, findings):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, start=1):
            for annotation in OLD_ANNOTATIONS:
                if annotation in line:
                    findings.append(f\"{OLD_ANNOTATIONS[annotation]} (File: {file_path}, Line: {i})\")

def scan_xml_file(file_path, findings):
    filename = os.path.basename(file_path)
    for key in XML_WARNINGS:
        if filename.endswith(key):
            findings.append(f\"{XML_WARNINGS[key]} (File: {file_path})\")

def write_report(findings):
    with open(\"modernization_report.md\", \"w\") as f:
        f.write(\"# Modernization Risk Report\\n\\n\")
        if not findings:
            f.write(\"✅ No legacy issues found.\\n\")
        for item in findings:
            f.write(f\"- {item}\\n\")

def scan_directory(root_dir):
    findings = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            path = os.path.join(dirpath, file)
            if file.endswith('.java'):
                scan_java_file(path, findings)
            elif file.endswith('.xml'):
                scan_xml_file(path, findings)
    write_report(findings)
    print(\"✅ Scan complete. See 'modernization_report.md'\")

if __name__ == \"__main__\":
    import sys
    if len(sys.argv) != 2:
        print(\"Usage: python scanner.py /path/to/java/project\")
    else:
        scan_directory(sys.argv[1])