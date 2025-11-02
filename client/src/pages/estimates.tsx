import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, Filter, Plus, Edit, Copy, Download, Trash2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Estimate {
  id: string;
  projectName: string;
  location: string;
  date: string;
  parts: number;
  amount: string;
  status: "draft" | "submitted" | "approved" | "archived";
}

const mockEstimates: Estimate[] = [
  {
    id: "1",
    projectName: "Highway Construction Phase 1",
    location: "Mumbai",
    date: "2025-01-28",
    parts: 3,
    amount: "₹45,00,000",
    status: "approved",
  },
  {
    id: "2",
    projectName: "Building Foundation Work",
    location: "Delhi",
    date: "2025-01-25",
    parts: 2,
    amount: "₹22,50,000",
    status: "submitted",
  },
  {
    id: "3",
    projectName: "Bridge Repair & Maintenance",
    location: "Bangalore",
    date: "2025-01-20",
    parts: 4,
    amount: "₹67,00,000",
    status: "draft",
  },
  {
    id: "4",
    projectName: "Road Expansion Project",
    location: "Pune",
    date: "2025-01-15",
    parts: 2,
    amount: "₹31,00,000",
    status: "approved",
  },
  {
    id: "5",
    projectName: "Drainage System Installation",
    location: "Chennai",
    date: "2025-01-10",
    parts: 3,
    amount: "₹18,50,000",
    status: "archived",
  },
];

export default function Estimates() {
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");

  const filteredEstimates = mockEstimates.filter((estimate) => {
    const matchesSearch = estimate.projectName.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         estimate.location.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "all" || estimate.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-3xl font-semibold">All Estimates</h1>
          <p className="text-sm text-muted-foreground mt-2">
            Manage and view all project estimates
          </p>
        </div>
        <Button data-testid="button-create-estimate">
          <Plus className="h-4 w-4 mr-2" />
          Create Estimate
        </Button>
      </div>

      <div className="flex gap-4 flex-wrap">
        <div className="relative flex-1 min-w-[250px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search estimates..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
            data-testid="input-search"
          />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[180px]" data-testid="select-status-filter">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="draft">Draft</SelectItem>
            <SelectItem value="submitted">Submitted</SelectItem>
            <SelectItem value="approved">Approved</SelectItem>
            <SelectItem value="archived">Archived</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Project Name</TableHead>
              <TableHead>Location</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Parts</TableHead>
              <TableHead>Total Amount</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredEstimates.length > 0 ? (
              filteredEstimates.map((estimate) => (
                <TableRow key={estimate.id} className="hover-elevate">
                  <TableCell className="font-medium" data-testid={`text-project-${estimate.id}`}>
                    {estimate.projectName}
                  </TableCell>
                  <TableCell className="text-sm">{estimate.location}</TableCell>
                  <TableCell className="text-sm">{estimate.date}</TableCell>
                  <TableCell className="text-sm">{estimate.parts}</TableCell>
                  <TableCell className="font-mono text-sm">{estimate.amount}</TableCell>
                  <TableCell>
                    <Badge variant="default" className="capitalize">
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
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-muted-foreground py-8">
                  No estimates found
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
