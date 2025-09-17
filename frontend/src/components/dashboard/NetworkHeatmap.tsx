import { heatmapData } from '@/data/dummyData';

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const hours = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'));

const getIntensityColor = (intensity: string, value: number) => {
  const opacity = Math.max(0.1, value / 100);
  
  switch (intensity) {
    case 'high':
      return `rgba(251, 146, 60, ${opacity})`;  // Orange
    case 'medium':
      return `rgba(34, 197, 94, ${opacity})`;   // Green
    case 'low':
      return `rgba(59, 130, 246, ${opacity})`;  // Blue
    default:
      return `rgba(156, 163, 175, ${opacity})`;  // Gray
  }
};

export const NetworkHeatmap = () => {
  return (
    <div className="bg-gradient-surface border border-border-muted rounded-lg p-6 shadow-md hover:shadow-lg transition-all duration-300 h-[500px] flex flex-col">
      <div className="mb-6 flex-shrink-0">
        <h3 className="text-xl font-heading font-semibold text-foreground mb-2">
          Network Activity Heatmap
        </h3>
        <p className="text-sm text-muted-foreground">
          Network traffic patterns over the past week
        </p>
      </div>

      <div className="relative flex-1 flex flex-col justify-center px-4">
        {/* Hour labels */}
        <div className="grid grid-cols-25 gap-0.5 mb-2">
          <div></div> {/* Empty space for day labels */}
          {hours.map((hour, index) => (
            <div 
              key={hour} 
              className="text-xs text-muted-foreground text-center"
              style={{ gridColumn: index + 2 }}
            >
              {index % 4 === 0 ? hour : ''}
            </div>
          ))}
        </div>

        {/* Heatmap grid */}
        <div className="space-y-1">
          {days.map((day, dayIndex) => (
            <div key={day} className="flex items-center gap-0.5">
              {/* Day label */}
              <div className="w-8 text-xs text-muted-foreground text-right pr-2">
                {day}
              </div>
              
              {/* Hour cells */}
              <div className="flex gap-0.5">
                {hours.map((hour, hourIndex) => {
                  const dataPoint = heatmapData.find(
                    (d) => d.x === hourIndex && d.y === dayIndex
                  );
                  
                  return (
                    <div
                      key={`${day}-${hour}`}
                      className="w-3 h-3 rounded-sm border border-border-muted/30 cursor-pointer transition-all duration-200 hover:scale-110 hover:border-primary/50 group relative"
                      style={{
                        backgroundColor: dataPoint 
                          ? getIntensityColor(dataPoint.intensity, dataPoint.value)
                          : 'rgba(156, 163, 175, 0.1)',
                      }}
                      title={`${day} ${hour}:00 - Activity: ${dataPoint?.value || 0}%`}
                    >
                      {/* Tooltip on hover */}
                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-card border border-border-muted rounded text-xs text-foreground opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                        {day} {hour}:00<br />
                        Activity: {dataPoint?.value || 0}%
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="mt-4 flex items-center justify-between">
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span>Less</span>
            <div className="flex gap-1">
              {[0.1, 0.3, 0.5, 0.7, 0.9].map((opacity, index) => (
                <div
                  key={index}
                  className="w-3 h-3 rounded-sm border border-border-muted/30"
                  style={{
                    backgroundColor: `rgba(251, 146, 60, ${opacity})`,
                  }}
                />
              ))}
            </div>
            <span>More</span>
          </div>
          
          <div className="flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: 'rgba(59, 130, 246, 0.8)' }} />
              <span className="text-muted-foreground">Low</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: 'rgba(34, 197, 94, 0.8)' }} />
              <span className="text-muted-foreground">Medium</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: 'rgba(251, 146, 60, 0.8)' }} />
              <span className="text-muted-foreground">High</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};