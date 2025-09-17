// Structured dummy data for the security dashboard

export interface VulnerabilityData {
  date: string;
  high: number;
  medium: number;
  low: number;
}

export interface AnomalyData {
  id: string;
  type: string;
  status: 'active' | 'resolved' | 'investigating';
  severity: 'high' | 'medium' | 'low';
  timestamp: string;
  description: string;
}

export interface NetworkData {
  id: string;
  ssid: string;
  bssid: string;
  channel: number;
  signalStrength: number;
  encryption: string;
  frequency: string;
  lastSeen: string;
  vendor: string;
  clients: number;
}

export interface EncryptionData {
  name: string;
  value: number;
  percentage: number;
  color: string;
}

export interface HeatmapData {
  x: number;
  y: number;
  value: number;
  intensity: 'low' | 'medium' | 'high';
}

// Vulnerability trend data (7 days)
export const vulnerabilityTrendData: VulnerabilityData[] = [
  { date: '2024-01-15', high: 12, medium: 28, low: 45 },
  { date: '2024-01-16', high: 15, medium: 32, low: 42 },
  { date: '2024-01-17', high: 8, medium: 35, low: 48 },
  { date: '2024-01-18', high: 18, medium: 29, low: 38 },
  { date: '2024-01-19', high: 22, medium: 31, low: 35 },
  { date: '2024-01-20', high: 14, medium: 38, low: 41 },
  { date: '2024-01-21', high: 11, medium: 33, low: 44 },
];

// Anomalies by status
export const anomalyStatusData: AnomalyData[] = [
  {
    id: 'ANM-001',
    type: 'Suspicious Network Activity',
    status: 'active',
    severity: 'high',
    timestamp: '2024-01-21T14:32:00Z',
    description: 'Unusual data exfiltration pattern detected on network segment 192.168.1.0/24'
  },
  {
    id: 'ANM-002',
    type: 'Unauthorized Access Attempt',
    status: 'investigating',
    severity: 'medium',
    timestamp: '2024-01-21T13:15:00Z',
    description: 'Multiple failed login attempts from IP 203.0.113.45'
  },
  {
    id: 'ANM-003',
    type: 'Malware Signature Detected',
    status: 'resolved',
    severity: 'high',
    timestamp: '2024-01-21T11:48:00Z',
    description: 'Trojan.GenKD detected and quarantined on workstation WS-047'
  },
  {
    id: 'ANM-004',
    type: 'Port Scanning Activity',
    status: 'active',
    severity: 'medium',
    timestamp: '2024-01-21T10:22:00Z',
    description: 'Systematic port scan detected from external IP range'
  },
  {
    id: 'ANM-005',
    type: 'Certificate Expiration',
    status: 'investigating',
    severity: 'low',
    timestamp: '2024-01-21T09:15:00Z',
    description: 'SSL certificate for mail.company.com expires in 7 days'
  },
  {
    id: 'ANM-006',
    type: 'Privilege Escalation',
    status: 'resolved',
    severity: 'high',
    timestamp: '2024-01-21T08:33:00Z',
    description: 'Unauthorized privilege escalation attempt blocked on server SRV-DB-01'
  }
];

// Network discovery data
export const networkData: NetworkData[] = [
  {
    id: 'NET-001',
    ssid: 'CorpWiFi-Main',
    bssid: '00:1B:44:11:3A:B7',
    channel: 6,
    signalStrength: -42,
    encryption: 'WPA3-Enterprise',
    frequency: '2.4GHz',
    lastSeen: '2024-01-21T14:45:00Z',
    vendor: 'Cisco Systems',
    clients: 127
  },
  {
    id: 'NET-002',
    ssid: 'CorpWiFi-Guest',
    bssid: '00:1B:44:11:3A:B8',
    channel: 11,
    signalStrength: -38,
    encryption: 'WPA2-PSK',
    frequency: '2.4GHz',
    lastSeen: '2024-01-21T14:44:00Z',
    vendor: 'Cisco Systems',
    clients: 23
  },
  {
    id: 'NET-003',
    ssid: 'NETGEAR_5G',
    bssid: '44:94:FC:72:84:A1',
    channel: 36,
    signalStrength: -55,
    encryption: 'WPA2-Mixed',
    frequency: '5GHz',
    lastSeen: '2024-01-21T14:42:00Z',
    vendor: 'Netgear Inc.',
    clients: 8
  },
  {
    id: 'NET-004',
    ssid: 'iPhone_Hotspot',
    bssid: 'A4:83:E7:15:C2:9F',
    channel: 1,
    signalStrength: -67,
    encryption: 'WPA2-PSK',
    frequency: '2.4GHz',
    lastSeen: '2024-01-21T14:41:00Z',
    vendor: 'Apple Inc.',
    clients: 1
  },
  {
    id: 'NET-005',
    ssid: 'LegacySystem',
    bssid: '00:0C:F1:56:98:AD',
    channel: 3,
    signalStrength: -73,
    encryption: 'WEP',
    frequency: '2.4GHz',
    lastSeen: '2024-01-21T14:30:00Z',
    vendor: 'D-Link Corporation',
    clients: 0
  },
  {
    id: 'NET-006',
    ssid: 'SecureLink-5G',
    bssid: 'B0:7F:B9:4E:21:33',
    channel: 149,
    signalStrength: -45,
    encryption: 'WPA3-SAE',
    frequency: '5GHz',
    lastSeen: '2024-01-21T14:43:00Z',
    vendor: 'ASUS',
    clients: 15
  }
];

// Encryption type distribution
export const encryptionTypeData: EncryptionData[] = [
  { name: 'WPA3', value: 245, percentage: 42, color: 'hsl(142 76% 36%)' },
  { name: 'WPA2', value: 186, percentage: 32, color: 'hsl(25 95% 53%)' },
  { name: 'WPA', value: 89, percentage: 15, color: 'hsl(38 92% 50%)' },
  { name: 'WEP', value: 35, percentage: 6, color: 'hsl(0 84% 60%)' },
  { name: 'Open', value: 29, percentage: 5, color: 'hsl(262 83% 58%)' }
];

// Network activity heatmap data (24x7 grid representing hours vs days)
export const generateHeatmapData = (): HeatmapData[] => {
  const data: HeatmapData[] = [];
  
  for (let day = 0; day < 7; day++) {
    for (let hour = 0; hour < 24; hour++) {
      // Simulate realistic network activity patterns
      let baseActivity = 0.3;
      
      // Business hours (9 AM - 6 PM) have higher activity
      if (hour >= 9 && hour <= 18 && day >= 1 && day <= 5) {
        baseActivity = 0.8;
      }
      
      // Evening hours have moderate activity
      if (hour >= 19 && hour <= 23) {
        baseActivity = 0.5;
      }
      
      // Add some randomness
      const noise = (Math.random() - 0.5) * 0.4;
      const activity = Math.max(0, Math.min(1, baseActivity + noise));
      
      let intensity: 'low' | 'medium' | 'high' = 'low';
      if (activity > 0.7) intensity = 'high';
      else if (activity > 0.4) intensity = 'medium';
      
      data.push({
        x: hour,
        y: day,
        value: Math.round(activity * 100),
        intensity
      });
    }
  }
  
  return data;
};

export const heatmapData = generateHeatmapData();