import { useEffect, useState } from "react";
import "./App.css";

const serviceInfo = {
  fraud: {
    name: "Fraud Detection",
    namespace: "fraud",
    endpoint: "assessment4-ying-fraud-endpoint",
  },
  recommendations: {
    name: "Recommendations",
    namespace: "recommendations",
    endpoint: "assessment4-ying-recommendations-endpoint",
  },
  forecasting: {
    name: "Forecasting",
    namespace: "forecasting",
    endpoint: "assessment4-ying-forecasting-endpoint",
  },
};

function App() {
  const [statuses, setStatuses] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch("http://localhost:8083/services");
        const data = await response.json();
        setStatuses(data);
      } catch (error) {
        console.error("Failed to fetch service status:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();

    const interval = setInterval(fetchStatus, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Assessment 4 ML Platform</h1>
        <p>Internal Kubernetes & SageMaker Service Dashboard</p>
      </header>

      <main>
        <section className="summary">
          <div>
            <span>3</span>
            <p>ML Services</p>
          </div>

          <div>
            <span>3</span>
            <p>EKS Namespaces</p>
          </div>

          <div>
            <span>3</span>
            <p>SageMaker Endpoints</p>
          </div>
        </section>

        <h2>Live Service Status</h2>

        <section className="service-grid">
          {Object.entries(serviceInfo).map(([key, service]) => {
            const status = statuses[key]?.status || "unknown";

            return (
              <div className="service-card" key={key}>
                <div className="card-header">
                  <h3>{service.name}</h3>

                  <span className={status === "healthy" ? "healthy" : "unhealthy"}>
                    {loading ? "Checking..." : status}
                  </span>
                </div>

                <p>
                  <strong>Namespace:</strong> {service.namespace}
                </p>

                <p>
                  <strong>SageMaker Endpoint:</strong>
                </p>

                <code>{service.endpoint}</code>

                <div className="architecture">
                  FastAPI → Pod Identity → SageMaker
                </div>
              </div>
            );
          })}
        </section>
      </main>
    </div>
  );
}

export default App;