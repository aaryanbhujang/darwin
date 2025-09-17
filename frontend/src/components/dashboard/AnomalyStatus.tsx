import { anomalyStatusData, type AnomalyData } from '@/data/dummyData';
import { Badge } from '@/components/ui/badge';
import { Clock, AlertTriangle, CheckCircle, Eye } from 'lucide-react';

const StatusIcon = ({ status }: { status: AnomalyData['status'] }) => {
  switch (status) {
    case 'active':
      return <AlertTriangle className="w-4 h-4 text-destructive" />;
    case 'resolved':
      return <CheckCircle className="w-4 h-4 text-success" />;
    case 'investigating':
      return <Eye className="w-4 h-4 text-warning" />;
    default:
      return <Clock className="w-4 h-4 text-muted-foreground" />;
  }
};

const SeverityBadge = ({ severity }: { severity: AnomalyData['severity'] }) => {
  const variants = {
    high: 'bg-destructive/10 text-destructive border-destructive/20',
    medium: 'bg-warning/10 text-warning border-warning/20',
    low: 'bg-success/10 text-success border-success/20',
  };

  return (
    <Badge className={`${variants[severity]} text-xs font-medium`}>
      {severity.toUpperCase()}
    </Badge>
  );
};

const StatusBadge = ({ status }: { status: AnomalyData['status'] }) => {
  const variants = {
    active: 'bg-destructive/10 text-destructive border-destructive/20',
    resolved: 'bg-success/10 text-success border-success/20',
    investigating: 'bg-warning/10 text-warning border-warning/20',
  };

  return (
    <Badge className={`${variants[status]} text-xs font-medium`}>
      {status.toUpperCase()}
    </Badge>
  );
};

export const AnomalyStatus = () => {
  return (
    <div className="bg-gradient-surface border border-border-muted rounded-lg p-6 shadow-md hover:shadow-lg transition-all duration-300 h-[500px] flex flex-col">
      <div className="mb-6 flex-shrink-0">
        <h3 className="text-xl font-heading font-semibold text-foreground mb-2">
          Security Anomalies
        </h3>
        <p className="text-sm text-muted-foreground">
          Recent security events and their current status
        </p>
      </div>

      <div className="space-y-3 overflow-y-auto flex-1 pr-2">
        {anomalyStatusData.map((anomaly, index) => (
          <div 
            key={anomaly.id}
            className="bg-surface border border-border-muted rounded-lg p-4 hover:border-primary/30 transition-all duration-200 cursor-pointer group"
            style={{
              animation: `slideInRight 0.3s ease-out ${index * 0.1}s both`
            }}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <StatusIcon status={anomaly.status} />
                <span className="font-medium text-sm text-foreground">
                  {anomaly.type}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <SeverityBadge severity={anomaly.severity} />
                <StatusBadge status={anomaly.status} />
              </div>
            </div>
            
            <p className="text-xs text-muted-foreground mb-2 leading-relaxed">
              {anomaly.description}
            </p>
            
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span className="font-mono">{anomaly.id}</span>
              <span>{new Date(anomaly.timestamp).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Add the animation keyframes to the CSS
const styles = `
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
`;

// Inject styles
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}