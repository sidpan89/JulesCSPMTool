# This file contains the raw SQL for creating and managing Row-Level Security (RLS) policies.
# These functions are designed to be executed once in an Alembic migration.

# The SQL to create a function that enables RLS on a specific table.
# This function creates a policy named 'tenant_isolation_policy' which ensures
# that users can only access rows that match their tenant_id.
# The tenant_id is retrieved from a session variable 'app.current_tenant'.
CREATE_ENABLE_RLS_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION enable_rls(table_name TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_name);
    EXECUTE format('
        CREATE POLICY tenant_isolation_policy ON public.%I
        FOR ALL
        USING (tenant_id = (SELECT current_setting(''app.current_tenant'', true))::uuid)
        WITH CHECK (tenant_id = (SELECT current_setting(''app.current_tenant'', true))::uuid);
    ', table_name, table_name);
END;
$$ LANGUAGE plpgsql;
"""

# The SQL to create a function that disables RLS on a specific table.
# This is useful for maintenance or if RLS needs to be removed.
CREATE_DISABLE_RLS_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION disable_rls(table_name TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('DROP POLICY IF EXISTS tenant_isolation_policy ON public.%I', table_name);
    EXECUTE format('ALTER TABLE public.%I DISABLE ROW LEVEL SECURITY', table_name);
END;
$$ LANGUAGE plpgsql;
"""

# A list of all tables that should have tenant isolation RLS enabled.
# The 'tenants' table itself is excluded because it needs to be accessible
# to find a tenant during login/signup before a tenant context is set.
RLS_ENABLED_TABLES = [
    "users",
    # Add other tenant-specific tables here as they are created
    # e.g., "cs_findings", "ci_findings", "subscriptions"
]
