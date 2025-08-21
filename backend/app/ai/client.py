from . import prompts
from app.products.cspm.models import CSPMFinding

class MockAIClient:
    """
    A mock AI client that simulates responses from a large language model.
    This is used to avoid making real API calls during development and testing.
    """
    def get_finding_explanation(self, finding: CSPMFinding) -> str:
        """
        Simulates a call to an AI model to get an explanation for a finding.
        Returns a hardcoded, templated response.
        """

        # In a real implementation, you would format the prompt with the finding's data
        # and send it to the AI API (e.g., OpenAI).
        #
        # prompt = prompts.EXPLAIN_FINDING_PROMPT_TEMPLATE.format(
        #     resource_id=finding.resource_id,
        #     severity=finding.severity,
        #     description=finding.description
        # )
        # response = openai.chat.completions.create(...)
        # return response.choices[0].message.content

        # For this mock, we return a hardcoded but informative string.
        mock_explanation = f"""
### **What is this finding?**

The security scan has identified a potential issue with the resource **{finding.resource_id}**.
Specifically, the issue is: *{finding.description}*.
This has been classified as a **{finding.severity}** severity risk.

### **What is the risk?**

If this issue is not addressed, it could be exploited by an attacker, potentially leading to unauthorized access to your systems, data breaches, or disruption of your services. Given the severity level, this should be investigated with appropriate priority.

### **How do I fix it?**

To remediate this finding, you should review the configuration of the identified resource. A general recommendation is to follow the principle of least privilege and apply the most restrictive settings possible that still allow for proper application function. For this specific issue, you should investigate how to [Corrective Action - e.g., 'apply a more restrictive security group', 'enable encryption', 'remove public access'].

Please consult your cloud provider's official documentation for detailed, step-by-step instructions on how to secure this resource.

---
*(This is a mock AI-generated response for demonstration purposes.)*
"""
        return mock_explanation

# Instantiate a singleton mock client to be used by the application
mock_ai_client = MockAIClient()
