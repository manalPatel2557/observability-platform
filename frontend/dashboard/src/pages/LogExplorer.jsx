import { useEffect, useState } from "react";
import { getLogs } from "../api/logsApi";

function LogExplorer() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    const data = await getLogs();
    setLogs(data.logs);
  };

  return (
    <div>
      <h2>Log Explorer</h2>

      {logs.map((log, index) => (
        <div key={index}>
          <strong>{log.service}</strong>
          {" | "}
          {log.level}
          {" | "}
          {log.message}
        </div>
      ))}
    </div>
  );
}

export default LogExplorer;
