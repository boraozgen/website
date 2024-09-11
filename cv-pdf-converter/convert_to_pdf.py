import subprocess
import os
from weasyprint import HTML

def merge_markdown_files(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as out:
        out.write(f1.read())
        out.write('\n\n')
        out.write(f2.read())

def markdown_to_html(input_file, output_file):
    subprocess.run(['pandoc', input_file, '-o', output_file])

def insert_content_into_template(template_file, content_file, output_file):
    with open(template_file, 'r') as template, open(content_file, 'r') as content, open(output_file, 'w') as output:
        template_html = template.read()
        content_html = content.read()
        
        # Replace placeholders in the template
        final_html = template_html.replace('{{CONTENT}}', content_html)
        
        output.write(final_html)

def html_to_pdf(input_file, output_file):
    HTML(input_file).write_pdf(output_file)

def main():
    # Hard-coded values
    output_filename = "bora-ozgen-cv"

    # Merge Markdown files
    merge_markdown_files('content/resume.md', 'cv-pdf-converter/cv_contact.md', 'temp_merged.md')

    # Convert merged Markdown to HTML
    markdown_to_html('temp_merged.md', 'temp_content.html')

    # Insert content into template
    insert_content_into_template('cv-pdf-converter/template.html', 'temp_content.html', f'{output_filename}.html')

    if not os.path.exists('cv-pdf-converter/output'):
        os.makedirs('cv-pdf-converter/output')

    # Convert final HTML to PDF using WeasyPrint
    html_to_pdf(f'{output_filename}.html', f'cv-pdf-converter/output/{output_filename}.pdf')

    # Clean up temporary files
    os.remove('temp_merged.md')
    os.remove('temp_content.html')
    os.remove(f'{output_filename}.html')

    print(f"Conversion complete. Output: {output_filename}.pdf")

if __name__ == "__main__":
    main()