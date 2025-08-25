# Admin Setup Checklist

This checklist provides a 10-step guide for administrators to get the AI Cloud Security Suite up and running for the first time.

1.  [ ] **Clone the Repository**
    *   Clone this repository to your local machine:
        ```bash
        git clone <repository-url>
        cd ai-sec-suite
        ```

2.  [ ] **Install Prerequisites**
    *   Ensure you have `Docker` and `Docker Compose` installed and running on your system.
    *   Ensure you have `make` installed.

3.  [ ] **Configure Backend Environment**
    *   Copy the backend environment variable template:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file and review the values. The defaults are suitable for local development, but you should provide a unique `SECRET_KEY`.

4.  [ ] **Configure Frontend Environment**
    *   Copy the frontend environment variable template:
        ```bash
        cp frontend/.env.example frontend/.env.local
        ```
    *   Verify that `NEXT_PUBLIC_API_BASE_URL` points to the correct backend URL (the default is `http://localhost:8000/api/v1`).

5.  [ ] **Verify Environment Setup**
    *   Run the environment verification script to ensure all required variables are set. First, make it executable:
        ```bash
        chmod +x scripts/verify_env.sh
        ./scripts/verify_env.sh
        ```

6.  [ ] **Build and Run Services**
    *   Start all application services using Docker Compose:
        ```bash
        make up
        ```
    *   This will build the containers and run them in the background. You can check the status with `docker-compose ps`.

7.  [ ] **Run Database Migrations**
    *   Apply all database migrations to set up the initial schema. This command runs Alembic inside the running backend container.
        ```bash
        make migrate
        ```

8.  [ ] **Seed Demo Data (Optional)**
    *   Run the seeding script to populate the database with a demo tenant and sample findings. First, make it executable:
        ```bash
        chmod +x scripts/seed_demo.sh
        ./scripts/seed_demo.sh
        ```

9.  [ ] **Access the Application**
    *   Open your browser and navigate to `http://localhost:3000` to see the application.
    *   The backend API documentation is available at `http://localhost:8000/docs`.
    *   You can sign up with a new account or log in with the demo account if you seeded the database (`testuser@example.com` / `password123`).

10. [ ] **Deploy Cloud Role (Azure)**
    *   To scan Azure resources, deploy the custom read-only role using the provided Bicep template. You must be logged into Azure with the `az` CLI.
        ```bash
        az deployment sub create --location <your-azure-location> --template-file scripts/azure_role.bicep
        ```
