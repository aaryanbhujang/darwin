import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { encryptionTypeData } from '@/data/dummyData';

const RADIAN = Math.PI / 180;

const renderCustomizedLabel = ({
  cx, cy, midAngle, innerRadius, outerRadius, percent
}: any) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  if (percent < 0.05) return null; // Don't show labels for very small slices

  return (
    <text 
      x={x} 
      y={y} 
      fill="white" 
      textAnchor={x > cx ? 'start' : 'end'} 
      dominantBaseline="central"
      fontSize="12"
      fontWeight="600"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-card border border-border-muted rounded-lg p-3 shadow-lg backdrop-blur-sm">
        <p className="text-sm font-medium mb-1">{data.name}</p>
        <p className="text-sm text-muted-foreground">
          {data.value} networks ({data.percentage}%)
        </p>
      </div>
    );
  }
  return null;
};

const CustomLegend = ({ payload }: any) => {
  return (
    <div className="flex flex-wrap justify-center gap-4 mt-4">
      {payload.map((entry: any, index: number) => (
        <div 
          key={`legend-${index}`} 
          className="flex items-center gap-2 text-sm"
        >
          <div 
            className="w-3 h-3 rounded-full border-2 border-background"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-foreground font-medium">{entry.value}</span>
          <span className="text-muted-foreground">
            ({encryptionTypeData.find(d => d.name === entry.value)?.percentage}%)
          </span>
        </div>
      ))}
    </div>
  );
};

export const EncryptionChart = () => {
  return (
    <div className="bg-gradient-surface border border-border-muted rounded-lg p-6 shadow-md hover:shadow-lg transition-all duration-300 h-[500px] flex flex-col">
      <div className="mb-6 flex-shrink-0">
        <h3 className="text-xl font-heading font-semibold text-foreground mb-2">
          Encryption Distribution
        </h3>
        <p className="text-sm text-muted-foreground">
          Security protocols used across detected networks
        </p>
      </div>
      
      <div className="flex-1 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={encryptionTypeData}
              cx="50%"
              cy="45%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={100}
              innerRadius={40}
              fill="#8884d8"
              dataKey="value"
              animationBegin={0}
              animationDuration={800}
            >
              {encryptionTypeData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend content={<CustomLegend />} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      
      {/* Summary stats */}
      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div className="bg-surface rounded-lg p-3 border border-border-muted">
          <p className="text-muted-foreground mb-1">Most Secure</p>
          <p className="font-semibold text-success">
            WPA3 ({encryptionTypeData[0].percentage}%)
          </p>
        </div>
        <div className="bg-surface rounded-lg p-3 border border-border-muted">
          <p className="text-muted-foreground mb-1">Vulnerable</p>
          <p className="font-semibold text-destructive">
            WEP + Open ({encryptionTypeData[3].percentage + encryptionTypeData[4].percentage}%)
          </p>
        </div>
      </div>
    </div>
  );
};