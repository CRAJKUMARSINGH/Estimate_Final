import { FileText, Folder, Calculator, Clock } from "lucide-react";
import DashboardCard from "../DashboardCard";

export default function DashboardCardExample() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <DashboardCard
        icon={Folder}
        label="Total Projects"
        value="12"
        subtitle="3 active"
      />
      <DashboardCard
        icon={FileText}
        label="Measurement Sheets"
        value="48"
        subtitle="15 pending"
      />
      <DashboardCard
        icon={Calculator}
        label="Total Estimated Cost"
        value="₹45.2L"
        subtitle="Across all projects"
      />
      <DashboardCard
        icon={Clock}
        label="Recent Activity"
        value="2h ago"
        subtitle="Last modified"
      />
    </div>
  );
}
