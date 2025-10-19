Generate a Markdown document using a Python script. Returns a markdown hyperlink for downloading the generated file.

Template structure:
```python
# Allowed packages
import numpy as np
import os
import pypandoc

# Import here other md packages you need, but do not import other packages that are not allowed.

# Path to save the Markdown file, previously defined in the server.py file
MD_PATH = md_path # Do not modify this line, it is defined in the server.py file

def markdown():
    # Build a Markdown document according to the user's request.
    markdown_content = "# Your Markdown Content Here"

    # Save the markdown
    pypandoc.convert_text(markdown_content, 'md', format='md', outputfile=MD_PATH, extra_args=['--standalone']) # Do not modify this line, it is defined in the server.py file

    # Check if the file was created successfully
    if not os.path.exists(MD_PATH):
        raise ValueError(f"Failed to create the Markdown file.")
    else:
        return f"Markdown file created successfully!"

# Invoke the function to generate the markdown document
markdown()
```

Provide a complete Python script following this template to generate your Markdown document.