import os

# Base directory for the Astro content
base_dir = "src/content/docs"

# Input site map
site_map = {
    "Map typologies": [
        "Microplanning",
        "Reference",
        "Comms / PR* (TBD)"
    ],
    "Template concept": [
        "Importing a PAGX file",
        "Project packages vs layouts",
        "Linking and relinking new source data"
    ],
    "Map series concept": {
        "Index layers": [
            "Overview",
            {
                "Naming schemes (see export best practices)": [
                    "A note on multipart polygons",
                    "“pageName” versus “page number” in ArcGIS functionality"
                ]
            },
            "[See preprocessing routine]",
            "Administrative nesting / dissolves",
            "Main angle calculation",
            "Page margins and map scale rounding",
            "Alternative to boundary polygons: grid index features tool"
        ]
    },
    # &c
}

# Helper function to create a directory
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Helper function to write Markdown files
def write_markdown_file(filepath, title, headers):
    with open(filepath, "w") as f:
        f.write(f"# {title}\n\n")
        f.write("This is a placeholder text for this section.\n\n")
        for header in headers:
            if isinstance(header, str):
                f.write(f"## {header}\n\nPlaceholder content.\n\n")
            elif isinstance(header, dict):
                for subheader, subsubheaders in header.items():
                    f.write(f"## {subheader}\n\nPlaceholder content.\n\n")
                    for subsub in subsubheaders:
                        f.write(f"### {subsub}\n\nPlaceholder content.\n\n")

# Recursively generate Markdown files
def process_site_map(site_map, parent_dir):
    for title, content in site_map.items():
        # Create a slug for the directory
        slug = title.lower().replace(" ", "-").replace("*", "").replace("/", "").strip()
        dir_path = os.path.join(parent_dir, slug)
        create_dir(dir_path)

        # Determine headers
        if isinstance(content, list):
            write_markdown_file(os.path.join(dir_path, "index.md"), title, content)
        elif isinstance(content, dict):
            write_markdown_file(os.path.join(dir_path, "index.md"), title, [])
            process_site_map(content, dir_path)

# Create base directory
create_dir(base_dir)

# Process the site map
process_site_map(site_map, base_dir)

print("Site map generated successfully!")
