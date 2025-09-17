import { useState } from 'react';
import { networkData, type NetworkData } from '@/data/dummyData';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Eye, Signal, Shield, Users, Wifi } from 'lucide-react';

const EncryptionBadge = ({ encryption }: { encryption: string }) => {
  const getVariant = (enc: string) => {
    if (enc.includes('WPA3')) return 'bg-success/10 text-success border-success/20';
    if (enc.includes('WPA2')) return 'bg-primary/10 text-primary border-primary/20';
    if (enc.includes('WPA')) return 'bg-warning/10 text-warning border-warning/20';
    if (enc.includes('WEP')) return 'bg-destructive/10 text-destructive border-destructive/20';
    return 'bg-muted/10 text-muted-foreground border-muted/20';
  };

  return (
    <Badge className={`${getVariant(encryption)} text-xs font-medium`}>
      {encryption}
    </Badge>
  );
};

const SignalStrength = ({ strength }: { strength: number }) => {
  const getColor = (str: number) => {
    if (str > -50) return 'text-success';
    if (str > -60) return 'text-warning';
    return 'text-destructive';
  };

  const getBars = (str: number) => {
    if (str > -50) return 4;
    if (str > -60) return 3;
    if (str > -70) return 2;
    return 1;
  };

  return (
    <div className="flex items-center gap-2">
      <Signal className={`w-4 h-4 ${getColor(strength)}`} />
      <span className="text-xs font-mono">{strength}dBm</span>
    </div>
  );
};

export const NetworksTable = () => {
  const [showAll, setShowAll] = useState(false);
  const displayedNetworks = showAll ? networkData : networkData.slice(0, 6);

  return (
    <div className="bg-gradient-surface border border-border-muted rounded-lg p-6 shadow-md hover:shadow-lg transition-all duration-300">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-xl font-heading font-semibold text-foreground">
            Discovered Networks
          </h3>
          <Badge className="bg-primary/10 text-primary border-primary/20 text-xs font-medium">
            {networkData.length} Networks
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground">
          Recently detected wireless networks and their security profiles
        </p>
      </div>

      <div className="overflow-hidden">
        <div className="space-y-3">
          {displayedNetworks.map((network, index) => (
            <div 
              key={network.id}
              className="bg-surface border border-border-muted rounded-lg p-4 hover:border-primary/30 transition-all duration-200 group"
              style={{
                animation: `fadeInUp 0.3s ease-out ${index * 0.05}s both`
              }}
            >
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Network Info */}
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Wifi className="w-4 h-4 text-primary" />
                    <span className="font-medium text-sm text-foreground">
                      {network.ssid}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground font-mono">
                    {network.bssid}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {network.vendor}
                  </p>
                </div>

                {/* Signal & Channel */}
                <div className="space-y-1">
                  <SignalStrength strength={network.signalStrength} />
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <span>Ch {network.channel}</span>
                    <span>•</span>
                    <span>{network.frequency}</span>
                  </div>
                </div>

                {/* Security */}
                <div className="space-y-2">
                  <EncryptionBadge encryption={network.encryption} />
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Users className="w-3 h-3" />
                    <span>{network.clients} clients</span>
                  </div>
                </div>

                {/* Last Seen */}
                <div className="text-right space-y-1">
                  <p className="text-xs text-muted-foreground">
                    {new Date(network.lastSeen).toLocaleString()}
                  </p>
                  <Button 
                    size="sm" 
                    variant="outline"
                    className="text-xs h-6 px-2 hover:bg-primary/10 hover:border-primary/30"
                  >
                    <Eye className="w-3 h-3 mr-1" />
                    Details
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {!showAll && networkData.length > 6 && (
          <div className="mt-4 text-center">
            <Button 
              variant="outline" 
              onClick={() => setShowAll(true)}
              className="hover:bg-primary/10 hover:border-primary/30"
            >
              See More ({networkData.length - 6} remaining)
            </Button>
          </div>
        )}

        {showAll && (
          <div className="mt-4 text-center">
            <Button 
              variant="outline" 
              onClick={() => setShowAll(false)}
              className="hover:bg-primary/10 hover:border-primary/30"
            >
              Show Less
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

// Add the animation keyframes
const styles = `
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
`;

if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}