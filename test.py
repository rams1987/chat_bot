import re

def subheading_matching(lines):
    """
    subheading matching using predefined patterns and regex.
    
    Args:
        lines (list of str): Lines of text to test against the subheading patterns.
    
    Returns:
        list of str: A list of results indicating whether each line is a subheading.
    """
    # Subheading titles to match
    subheading_patterns = [
        r"Initial Financial Insights and Recommendations",
        r"Evaluating Your Current Situation",
        r"Detailed Budget Analysis & Recommendations",
        r"Actionable Steps & Long-Term Planning",
        r"Warnings and Areas of Concern",
        r"Next Steps"
    ]

    # Escape special characters for regex safety
    escaped_patterns = [re.escape(p) for p in subheading_patterns]

    # Regex pattern to match optional **, numbering, and subheading titles
    subheading_regex = re.compile(
    r"^\s*\-?\s*\**\s*(\d+\.\s*)?(%s)\s*\**\s*$" % "|".join(escaped_patterns),
    re.IGNORECASE
    )

    return subheading_regex.match(lines.strip())

    # results = []
    # for line in lines:
    #     match = subheading_regex.match(line.strip())
    #     if match:
    #         results.append(f"✅ Matched Subheading: '{line}'")
    #     else:
    #         results.append(f"❌ Not a Subheading:    '{line}'")
    
    # return results

# Example usage
if __name__ == "__main__":
    test_lines = [
        "- 1. Initial Financial Insights and Recommendations",
        "- 2. Evaluating Your Current Situation",
        "- 3. Detailed Budget Analysis & Recommendations",
        "Actionable Steps & Long-Term Planning",
        "Warnings and Areas of Concern",
        "Next Steps",
        "- This is a bullet point",
        "This is a normal paragraph."
    ]
    results = subheading_matching(test_lines)
    for result in results:
        print(result)
