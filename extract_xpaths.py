"""
Script to extract all XPaths of elements from a webpage using Selenium
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime

# ============================================
# CONFIGURATION - UPDATE THIS URL
# ============================================
TARGET_URL = "https://lacps--qa1.sandbox.my.site.com/s/"  # Change to your target URL

# Output file for XPaths
OUTPUT_FILE = "extracted_xpaths.json"


def get_xpath(element, driver):
    """Generate XPath for an element using JavaScript"""
    script = """
    function getXPath(element) {
        if (element.id !== '') {
            return '//*[@id="' + element.id + '"]';
        }
        if (element === document.body) {
            return '/html/body';
        }
        var ix = 0;
        var siblings = element.parentNode ? element.parentNode.childNodes : [];
        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element) {
                var parentPath = element.parentNode ? getXPath(element.parentNode) : '';
                var tagName = element.tagName.toLowerCase();
                return parentPath + '/' + tagName + '[' + (ix + 1) + ']';
            }
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                ix++;
            }
        }
    }
    return getXPath(arguments[0]);
    """
    try:
        return driver.execute_script(script, element)
    except:
        return None


def get_element_info(element, driver):
    """Extract information about an element"""
    try:
        xpath = get_xpath(element, driver)
        if not xpath:
            return None
            
        return {
            "xpath": xpath,
            "tag": element.tag_name,
            "id": element.get_attribute("id") or "",
            "class": element.get_attribute("class") or "",
            "name": element.get_attribute("name") or "",
            "type": element.get_attribute("type") or "",
            "text": element.text[:100] if element.text else "",  # Limit text length
            "href": element.get_attribute("href") or "",
            "placeholder": element.get_attribute("placeholder") or "",
        }
    except Exception as e:
        return None


def extract_xpaths(url):
    """Extract all XPaths from a webpage"""
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize driver
    print(f"Starting browser...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        driver.implicitly_wait(5)
        
        # Get page title
        page_title = driver.title
        print(f"Page Title: {page_title}")
        
        # Find all elements
        print("Extracting elements...")
        all_elements = driver.find_elements(By.XPATH, "//*")
        print(f"Found {len(all_elements)} total elements")
        
        # Extract info for each element
        elements_data = []
        interactive_elements = []
        
        for element in all_elements:
            info = get_element_info(element, driver)
            if info:
                elements_data.append(info)
                
                # Separate interactive elements
                if info["tag"] in ["input", "button", "a", "select", "textarea", "label"]:
                    interactive_elements.append(info)
        
        # Prepare output
        output = {
            "url": url,
            "title": page_title,
            "extracted_at": datetime.now().isoformat(),
            "total_elements": len(elements_data),
            "interactive_count": len(interactive_elements),
            "interactive_elements": interactive_elements,
            "all_elements": elements_data
        }
        
        # Save to JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Extracted {len(elements_data)} elements")
        print(f"✓ Found {len(interactive_elements)} interactive elements")
        print(f"✓ Saved to: {OUTPUT_FILE}")
        
        # Print summary of interactive elements
        print(f"\n=== Interactive Elements Summary ===")
        print(f"{'Tag':<10} {'ID/Name':<30} {'XPath'}")
        print("-" * 100)
        
        for elem in interactive_elements[:20]:  # Show first 20
            identifier = elem["id"] or elem["name"] or elem["text"][:20] or "(no id)"
            print(f"{elem['tag']:<10} {identifier:<30} {elem['xpath'][:60]}")
        
        if len(interactive_elements) > 20:
            print(f"... and {len(interactive_elements) - 20} more (see {OUTPUT_FILE})")
        
        return output
        
    finally:
        driver.quit()
        print("\n✓ Browser closed")


if __name__ == "__main__":
    extract_xpaths(TARGET_URL)
