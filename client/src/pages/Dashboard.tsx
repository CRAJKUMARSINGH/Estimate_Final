import { FileText, Folder, Calculator, Clock, Plus } from "lucide-react";
import DashboardCard from "@/components/DashboardCard";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from "@/components/ui/card";

export default function Dashboard() {
  const recentProjects = [
    {
      id: "1",
      name: "Commercial Complex - Panchayat Samiti Girwa",
      location: "Girwa, Udaipur",
      estimatedCost: "₹12,45,000",
      status: "In Progress",
      lastModified: "2 hours ago",
    },
    {
      id: "2",
      name: "Community Hall Construction",
      location: "Mavli, Udaipur",
      estimatedCost: "₹8,75,000",
      status: "Pending Review",
      lastModified: "1 day ago",
    },
    {
      id: "3",
      name: "School Building Renovation",
      location: "Bhinder, Udaipur",
      estimatedCost: "₹15,20,000",
      status: "Completed",
      lastModified: "3 days ago",
    },
  ];

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Overview of your estimation projects
          </p>
        </div>
        <Button data-testid="button-new-project">
          <Plus className="h-4 w-4 mr-2" />
          New Project
        </Button>
      </div>

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

      <Card className="overflow-hidden">
        <div className="bg-muted/50 px-6 py-4 border-b">
          <h3 className="text-lg font-semibold">Recent Projects</h3>
        </div>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/30">
                <TableHead className="text-xs font-semibold uppercase tracking-wide">
                  Project Name
                </TableHead>
                <TableHead className="text-xs font-semibold uppercase tracking-wide">
                  Location
                </TableHead>
                <TableHead className="text-right text-xs font-semibold uppercase tracking-wide">
                  Estimated Cost
                </TableHead>
                <TableHead className="text-xs font-semibold uppercase tracking-wide">
                  Status
                </TableHead>
                <TableHead className="text-xs font-semibold uppercase tracking-wide">
                  Last Modified
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recentProjects.map((project, index) => (
                <TableRow
                  key={project.id}
                  className={index % 2 === 0 ? "bg-background" : "bg-muted/20"}
                  data-testid={`row-project-${project.id}`}
                >
                  <TableCell className="font-medium">{project.name}</TableCell>
                  <TableCell className="text-muted-foreground">
                    {project.location}
                  </TableCell>
                  <TableCell className="text-right font-mono font-medium">
                    {project.estimatedCost}
                  </TableCell>
                  <TableCell>
                    <span
                      className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium ${
                        project.status === "In Progress"
                          ? "bg-primary/10 text-primary"
                          : project.status === "Completed"
                          ? "bg-green-500/10 text-green-700 dark:text-green-400"
                          : "bg-amber-500/10 text-amber-700 dark:text-amber-400"
                      }`}
                    >
                      {project.status}
                    </span>
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {project.lastModified}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
