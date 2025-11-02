import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Edit, Copy, Download, Trash2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Estimate {
  id: string;
  projectName: string;
  date: string;
  parts: number;
  amount: string;
  status: "draft" | "submitted" | "approved";
}

const mockEstimates: Estimate[] = [
  {
    id: "1",
    projectName: "Highway Construction Phase 1",
    date: "2025-01-28",
    parts: 3,
    amount: "₹45,00,000",
    status: "approved",
  },
  {
    id: "2",
    projectName: "Building Foundation Work",
    date: "2025-01-25",
    parts: 2,
    amount: "₹22,50,000",
    status: "submitted",
  },
  {
    id: "3",
    projectName: "Bridge Repair & Maintenance",
    date: "2025-01-20",
    parts: 4,
    amount: "₹67,00,000",
    status: "draft",
  },
];

const statusColors = {
  draft: "default",
  submitted: "secondary",
  approved: "default",
} as const;

export function RecentEstimates() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Estimates</CardTitle>
        <CardDescription>View and manage your project estimates</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Project Name</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Parts</TableHead>
                <TableHead>Total Amount</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockEstimates.map((estimate) => (
                <TableRow key={estimate.id} className="hover-elevate">
                  <TableCell className="font-medium" data-testid={`text-project-${estimate.id}`}>
                    {estimate.projectName}
                  </TableCell>
                  <TableCell className="text-sm">{estimate.date}</TableCell>
                  <TableCell className="text-sm">{estimate.parts}</TableCell>
                  <TableCell className="font-mono text-sm">{estimate.amount}</TableCell>
                  <TableCell>
                    <Badge variant={statusColors[estimate.status]} className="capitalize">
                      {estimate.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex gap-2 justify-end">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => console.log('Edit:', estimate.id)}
                        data-testid={`button-edit-${estimate.id}`}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => console.log('Duplicate:', estimate.id)}
                        data-testid={`button-duplicate-${estimate.id}`}
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => console.log('Download:', estimate.id)}
                        data-testid={`button-download-${estimate.id}`}
                      >
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => console.log('Delete:', estimate.id)}
                        data-testid={`button-delete-${estimate.id}`}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
