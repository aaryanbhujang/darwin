import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { AlertTriangle, Wifi } from "lucide-react";
import { Users, Eye } from "lucide-react";

interface Finding {
  essid: string | null;
  bssid: string | null;
  issue: string | null;
}

export default function Index() {
  const [logs, setLogs] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/results/stats")
      .then((res) => res.json())
      .then((data) => setLogs(data))
      .catch((err) => console.error("Error fetching logs:", err));
  }, []);

  if (!logs) return <p className="text-center text-gray-400">Loading data...</p>;

  // colors for pie chart
  const COLORS = ["#ff6b6b", "#4dabf7", "#63e6be", "#ffd43b", "#845ef7"];

  // helper to render severity
// helper to render encryption badges
const getEncryptionBadge = (issue: string | null) => {
  const encryption = issue || "OPEN";
  const baseClasses = "px-3 py-1 text-xs font-semibold rounded-md border";

  if (encryption.includes("WPA3")) return <Badge className={`${baseClasses} bg-green-900/50 text-green-300 border-green-700`}>{encryption}</Badge>;
  if (encryption.includes("WPA2")) return <Badge className={`${baseClasses} bg-orange-900/50 text-orange-300 border-orange-700`}>{encryption}</Badge>;
  if (encryption.includes("WEP")) return <Badge className={`${baseClasses} bg-red-900/50 text-red-300 border-red-700`}>{encryption}</Badge>;
  if (encryption.includes("OPEN")) return <Badge className={`${baseClasses} bg-gray-700 text-gray-300 border-gray-600`}>OPEN</Badge>;
  
  return <Badge variant="outline">{encryption}</Badge>;
};

  return (
    <div className="p-6 space-y-6 bg-black min-h-screen text-white">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        🚀 Security Dashboard
      </h1>

      {/* --- Metrics --- */}
      <div className="grid grid-cols-3 gap-4">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-4">
            <p className="text-sm text-gray-400">Total APs</p>
            <p className="text-2xl font-bold">{logs.metrics.total_aps}</p>
          </CardContent>
        </Card>
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-4">
            <p className="text-sm text-gray-400">Vulnerable APs</p>
            <p className="text-2xl font-bold">{logs.metrics.vulnerable_aps}</p>
          </CardContent>
        </Card>
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-4">
            <p className="text-sm text-gray-400">Risk Score (%)</p>
            <p className="text-2xl font-bold">{logs.metrics.risk_score}</p>
          </CardContent>
        </Card>
      </div>

      {/* --- Charts + Anomalies Layout --- */}
      <div className="grid grid-cols-2 gap-4">
        {/* Left side: line + pie stacked */}
        <div className="space-y-4">
          {/* Line chart */}
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-4">
              <h2 className="text-lg font-semibold mb-2">Encryption Trends</h2>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart
                  data={logs.line_chart}
                  margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis
                    dataKey="time"
                    stroke="#aaa"
                    tickFormatter={(t) =>
                      new Date(t).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
                    }
                  />
                  <YAxis stroke="#aaa" />
                  <Tooltip
                    labelFormatter={(t) => new Date(t).toLocaleString()}
                  />
                  {logs.line_chart.length > 0 &&
                    Object.keys(logs.line_chart[0])
                      .filter((key) => key !== "time")
                      .map((enc, idx) => (
                        <Line
                          key={enc}
                          type="monotone"
                          dataKey={enc}
                          stroke={COLORS[idx % COLORS.length]}
                          strokeWidth={2}
                          dot={{ r: 3 }}
                          activeDot={{ r: 5 }}
                        />
                      ))}
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Pie chart */}
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-4">
              <h2 className="text-lg font-semibold mb-2">Network Types</h2>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={Object.entries(logs.pie_chart).map(([name, value]) => ({
                      name,
                      value,
                    }))}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label
                  >
                    {Object.entries(logs.pie_chart).map((_, idx) => (
                      <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Right side: Anomalies with sticky header */}
        <Card className="bg-gray-900 border-gray-800 shadow-lg h-full max-h-[600px] flex flex-col">
          <CardContent className="p-0 flex flex-col h-full">
            {/* Sticky Header */}
            <div className="p-6 border-b border-gray-800 sticky top-0 bg-gray-900 z-10">
              <h2 className="text-xl font-bold">Security Anomalies</h2>
              <p className="text-sm text-gray-400">
                Recent security events and their current status
              </p>
            </div>

            {/* Scrollable list */}
            <div className="p-6 space-y-4 overflow-y-auto">
              {logs.anomalies.length === 0 ? (
                <p className="text-gray-400">No anomalies detected 🎉</p>
              ) : (
                logs.anomalies.map((anom: string, i: number) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl bg-gray-800 border border-gray-700 flex items-start justify-between"
                  >
                    <div className="flex gap-3">
                      <AlertTriangle className="text-red-500 mt-1" size={20} />
                      <div>
                        <h3 className="font-semibold">{anom}</h3>
                        <p className="text-xs text-gray-400">Detected anomaly in Wi-Fi scan</p>
                        <p className="text-xs text-gray-500">ID: ANM-{i + 1}</p>
                      </div>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <Badge className="bg-red-600">HIGH</Badge>
                      <Badge className="bg-green-600">ACTIVE</Badge>
                      <p className="text-xs text-gray-500">{new Date().toLocaleString()}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* --- Discovered Networks (below) --- */}
      <Card className="bg-gray-900 border-gray-800 shadow-lg mt-4">
        <CardContent className="p-6">
          <div className="flex justify-between items-center mb-4">
            <div>
                <h2 className="text-xl font-bold">Discovered Networks</h2>
                <p className="text-sm text-gray-400">Recently detected wireless networks and their security profiles</p>
            </div>
            <Badge variant="secondary">{logs.findings.length} Networks</Badge>
          </div>
          <div className="space-y-3">
            {logs.findings.length === 0 ? (
              <p className="text-gray-400">No networks found</p>
            ) : (
              logs.findings.map((net: Finding, i: number) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all">
                  
                  {/* Left: Network Info */}
                  <div className="flex items-center gap-4 w-1/4">
                    <Wifi className="text-blue-400 flex-shrink-0" size={24} />
                    <div>
                      <h3 className="font-semibold text-white">{net.essid || "Unknown SSID"}</h3>
                      <p className="text-xs text-gray-400 font-mono tracking-tighter">{net.bssid}</p>
                      {/* Placeholder for Manufacturer - NOT in your current data */}
                      <p className="text-xs text-gray-500">Unknown Manufacturer</p>
                    </div>
                  </div>

                  {/* Middle: Technical Details */}
                  <div className="flex items-center justify-start gap-8 w-1/2">
                    {/* Placeholder for Signal - NOT in your current data */}
                    <p className="text-sm w-24"><strong>-50dBm</strong></p>
                    {/* Placeholder for Channel - NOT in your current data */}
                    <p className="text-sm text-gray-400 w-36">Ch 1 &bull; 2.4GHz</p>
                    
                    {/* This uses the 'issue' field for encryption */}
                    {getEncryptionBadge(net.issue)}

                    {/* Placeholder for Clients - NOT in your current data */}
                    <div className="flex items-center gap-2 text-sm text-gray-400">
                        <Users size={14} />
                        <span>-- clients</span>
                    </div>
                  </div>

                  {/* Right: Timestamp & Actions */}
                  <div className="flex items-center justify-end gap-4 w-1/4">
                    <p className="text-xs text-gray-400">{new Date().toLocaleString()}</p>
                    <button className="flex items-center gap-1.5 text-sm text-gray-400 hover:text-white transition-colors p-2 rounded-md hover:bg-gray-700">
                      <Eye size={14} /> Details
                    </button>
                  </div>

                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>


    </div>
  );
}
