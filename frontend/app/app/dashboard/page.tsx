const DashboardPage = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <p className="mt-4 text-gray-600">
        Welcome to your AI Cloud Security Suite dashboard.
      </p>
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded-lg shadow">
          <h2 className="text-xl font-semibold">CSPM Findings</h2>
          <p className="mt-2 text-4xl font-bold">12</p>
          <p className="text-sm text-gray-500">Open critical issues</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow">
          <h2 className="text-xl font-semibold">CIEM Identities</h2>
          <p className="mt-2 text-4xl font-bold">5</p>
          <p className="text-sm text-gray-500">Over-privileged users</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow">
          <h2 className="text-xl font-semibold">Active Scans</h2>
          <p className="mt-2 text-4xl font-bold">2</p>
          <p className="text-sm text-gray-500">Currently running</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
