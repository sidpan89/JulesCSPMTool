# This file contains templates for the prompts sent to the AI model.
# Separating prompts from the application logic makes them easier to manage and version.

EXPLAIN_FINDING_PROMPT_TEMPLATE = """
You are a world-class cloud security expert acting as a helpful assistant.
A security finding has been detected in our cloud environment.

Please provide a clear, concise, and helpful explanation for the following security finding.
Your explanation should be easy for a non-expert to understand and should cover three main points:
1.  **What is this finding?** (Explain the issue in simple terms)
2.  **What is the risk?** (Describe the potential impact if this is not addressed)
3.  **How do I fix it?** (Provide a high-level, actionable recommendation)

**Finding Details:**
- **Resource:** `{resource_id}`
- **Severity:** `{severity}`
- **Description:** `{description}`

Please structure your response clearly.
"""

# Example of another prompt template that could be added later
REMEDIATION_SNIPPET_PROMPT_TEMPLATE = """
You are a cloud security expert and a skilled programmer.
Based on the following security finding, generate a code snippet for remediation.
Provide the snippet in the most appropriate language (e.g., bash, PowerShell, Python).

**Finding Details:**
- **Resource:** `{resource_id}`
- **Cloud Provider:** `{cloud_provider}`
- **Description:** `{description}`

**Remediation Snippet:**
"""
