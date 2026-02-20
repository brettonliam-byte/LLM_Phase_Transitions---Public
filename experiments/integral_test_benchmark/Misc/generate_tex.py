import re

source_file = "Integral Test.txt"
output_file = "Integral_Test_Verbatim.tex"

header = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{geometry}
\usepackage{fancyvrb}
\geometry{a4paper, margin=1in}
\title{Integral Test Transcripts}
\author{}
\date{}

\begin{document}
\maketitle

"""

footer = r"""
\end{document}
"""

def clean_text(text):
    # minimal cleaning if necessary, but for verbatim we usually don't touch it
    # except maybe valid utf-8
    return text

try:
    with open(source_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Split roughly by known model headers or structure
    # We'll use a regex to identify lines that look like model headers
    # Heuristic: headers often don't end with punctuation, are short, and are followed by text.
    # But to be safe and strictly preserve content, let's just dump chunks.
    
    # Actually, the user wants a latex version.
    # Let's try to identify sections to make it look nice, but fallback to verbatim.
    
    latex_content = header
    
    # We will treat the whole file as a sequence of text.
    # To make it readable, we can wrap the whole thing in verbatim, 
    # OR we can try to be smart. 
    # Given the user's previous frustration, "exact information present" implies high fidelity.
    # Let's wrap the intro in normal text (escaping chars) and the rest in verbatim sections?
    # Or simpler: Just one big Verbatim environment? No, that's ugly.
    
    # Let's find the start of the models.
    # "Test and copy/paste transcripts here." seems to be the divider.
    
    split_marker = "Test and copy/paste transcripts here."
    
    if split_marker in content:
        intro, transcripts = content.split(split_marker, 1)
        
        # Process Intro
        latex_content += r"\section*{Introduction}" + "\n"
        # Simple escaping for intro text
        intro_safe = intro.replace('\\', r'\\textbackslash').replace('_', r'\_').replace('^', r'\^').replace('%', r'\%').replace('$', r'\$').replace('#', r'\#')
        latex_content += intro_safe + "\n"
        latex_content += r"\textbf{Test and copy/paste transcripts here.}" + "\n\n"
        
        # Process Transcripts
        # We will try to split by double newlines to find paragraphs, 
        # but to keep it "verbatim" style, let's just put it in a listings/verbatim env.
        
        latex_content += r"\section*{Transcripts}" + "\n"
        latex_content += r"\begin{verbatim}" + "\n"
        latex_content += transcripts.strip()
        latex_content += "\n" + r"\end{verbatim}" + "\n"
        
    else:
        # Fallback if marker not found: dump everything in verbatim
        latex_content += r"\begin{verbatim}" + "\n"
        latex_content += content
        latex_content += "\n" + r"\end{verbatim}" + "\n"

    latex_content += footer

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"Successfully generated {output_file}")

except Exception as e:
    print(f"Error: {e}")
