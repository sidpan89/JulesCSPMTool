# AI Cloud Security Subscription Suite

This repository contains the source code for a multi-product, subscription-based AI cloud security SaaS platform. It is designed to be an enterprise-grade solution for SMBs and mid-market customers, offering a portfolio of AI-powered cloud security products.

## Core Products

1.  **CSPM-Lite**: AI-driven cloud security posture management.
2.  **CIEM-Lite**: Cloud identity and entitlement management.
3.  **KSPM-Lite**: Kubernetes security posture management.
4.  **SecretGuard**: Secret scanning and management.
5.  **AttackPath View**: Attack path analysis and visualization.
6.  **Compliance Reporter**: Automated compliance reporting.

## Getting Started

### Prerequisites

*   Docker and Docker Compose
*   `make`
*   An OpenAI API key (optional, for AI features)
*   A Stripe account and API keys (optional, for billing features)

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/ai-sec-suite.git
    cd ai-sec-suite
    ```

2.  **Configure environment variables:**
    Copy the example environment files:
    ```bash
    cp .env.example .env
    cp frontend/.env.example frontend/.env.local
    ```
    Update the `.env` and `frontend/.env.local` files with your specific settings (e.g., database credentials, API keys).

3.  **Build and run the services:**
    ```bash
    make up
    ```
    This will start the backend, frontend, database, cache, and object storage services using Docker Compose.

4.  **Apply database migrations:**
    ```bash
    make migrate
    ```

5.  **Seed demo data (optional):**
    To populate the database with some sample data for a demo tenant:
    ```bash
    ./scripts/seed_demo.sh
    ```

6.  **Access the application:**
    *   **Frontend (Marketing Site):** [http://localhost:3000](http://localhost:3000)
    *   **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
