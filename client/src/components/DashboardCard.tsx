import { LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/card";

interface DashboardCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  subtitle?: string;
  iconColor?: string;
}

export default function DashboardCard({
  icon: Icon,
  label,
  value,
  subtitle,
  iconColor = "text-primary",
}: DashboardCardProps) {
  return (
    <Card className="p-6" data-testid={`card-${label.toLowerCase().replace(/\s+/g, '-')}`}>
      <div className="flex items-start gap-4">
        <div className={`rounded-lg bg-muted p-3 ${iconColor}`}>
          <Icon className="h-5 w-5" />
        </div>
        <div className="flex-1 space-y-1">
          <p className="text-sm font-medium text-muted-foreground">{label}</p>
          <p className="text-2xl font-semibold" data-testid={`text-${label.toLowerCase().replace(/\s+/g, '-')}-value`}>
            {value}
          </p>
          {subtitle && (
            <p className="text-xs text-muted-foreground">{subtitle}</p>
          )}
        </div>
      </div>
    </Card>
  );
}
