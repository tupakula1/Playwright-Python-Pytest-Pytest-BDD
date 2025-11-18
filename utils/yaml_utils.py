import yaml 
from pathlib import Path 
 
def load_yaml(file_path: str):
    """Load and return YAML content."""
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def get_locator(page_name: str, locator_name: str):
              
    """ Return locator for given page and key.
    Example: get_locator("home_page", "alt_logo") """
    
    yaml_path = f"testdata/locators/{page_name}.yaml"
    data = load_yaml(yaml_path)

    if page_name not in data:
        raise KeyError(f"Page '{page_name}' not found in YAML")

    page_locators = data[page_name]

    if locator_name not in page_locators:
        raise KeyError(f"Locator '{locator_name}' not found in page '{page_name}' section")

    return page_locators[locator_name]