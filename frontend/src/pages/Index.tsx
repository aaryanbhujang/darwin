import { VulnerabilityChart } from '@/components/dashboard/VulnerabilityChart';
import { AnomalyStatus } from '@/components/dashboard/AnomalyStatus';
import { NetworksTable } from '@/components/dashboard/NetworksTable';
import { NetworkHeatmap } from '@/components/dashboard/NetworkHeatmap';
import { EncryptionChart } from '@/components/dashboard/EncryptionChart';
import { Shield, Activity, Network, AlertTriangle } from 'lucide-react';

const DashboardHeader = () => (
  <header className="mb-8">
    <div className="flex items-center gap-3 mb-4">
      <div className="p-2 bg-primary/10 rounded-lg border border-primary/20">
        <Shield className="w-6 h-6 text-primary" />
      </div>
      <div>
        <h1 className="text-3xl font-heading font-bold text-foreground">
          Security Dashboard
        </h1>
        <p className="text-muted-foreground">
          Real-time network security monitoring and analysis
        </p>
      </div>
    </div>
    
    {/* Status indicators */}
    <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
      <div className="bg-gradient-surface border border-border-muted rounded-lg p-4 hover:shadow-md transition-all duration-200">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-success/10 rounded-lg">
            <Network className="w-5 h-5 text-success" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Networks</p>
            <p className="text-xl font-semibold text-foreground">23</p>
          </div>
        </div>
      </div>
      
      <div className="bg-gradient-surface border border-border-muted rounded-lg p-4 hover:shadow-md transition-all duration-200">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-warning/10 rounded-lg">
            <AlertTriangle className="w-5 h-5 text-warning" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Active Threats</p>
            <p className="text-xl font-semibold text-foreground">7</p>
          </div>
        </div>
      </div>
      
      <div className="bg-gradient-surface border border-border-muted rounded-lg p-4 hover:shadow-md transition-all duration-200">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg">
            <Activity className="w-5 h-5 text-primary" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Vulnerabilities</p>
            <p className="text-xl font-semibold text-foreground">142</p>
          </div>
        </div>
      </div>
      
      <div className="bg-gradient-surface border border-border-muted rounded-lg p-4 hover:shadow-md transition-all duration-200">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-destructive/10 rounded-lg">
            <Shield className="w-5 h-5 text-destructive" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Risk Score</p>
            <p className="text-xl font-semibold text-foreground">High</p>
          </div>
        </div>
      </div>
    </div>
  </header>
);

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-6 py-8 max-w-7xl">
        <DashboardHeader />
        
        {/* First section: Two columns - Vulnerability Chart & Anomaly Status */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <VulnerabilityChart />
          <AnomalyStatus />
        </div>
        
        {/* Second section: Two columns - Heatmap (2 cols), Encryption Chart (1 col) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <NetworkHeatmap />
          </div>
          <EncryptionChart />
        </div>
        
        {/* Third section: Full width - Networks Table */}
        <div className="mb-8">
          <NetworksTable />
        </div>
        
        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-border-muted">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <p>Last updated: {new Date().toLocaleString()}</p>
            <p>Security Dashboard v2.1</p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Index;
