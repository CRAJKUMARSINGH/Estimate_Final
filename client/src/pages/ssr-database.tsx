import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Search, Plus, Edit, Trash2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface SSRItem {
  id: string;
  code: string;
  description: string;
  unit: string;
  rate: string;
  category: string;
}

const mockSSRItems: SSRItem[] = [
  {
    id: "1",
    code: "SSR-001",
    description: "Excavation in all types of soil",
    unit: "cum",
    rate: "150.00",
    category: "Earthwork",
  },
  {
    id: "2",
    code: "SSR-002",
    description: "Plain Cement Concrete 1:4:8 (40mm nominal size)",
    unit: "cum",
    rate: "4,500.00",
    category: "Concrete",
  },
  {
    id: "3",
    code: "SSR-003",
    description: "Reinforced Cement Concrete M20",
    unit: "cum",
    rate: "6,800.00",
    category: "Concrete",
  },
  {
    id: "4",
    code: "SSR-004",
    description: "Brick work in cement mortar 1:6",
    unit: "sqm",
    rate: "580.00",
    category: "Masonry",
  },
  {
    id: "5",
    code: "SSR-005",
    description: "Steel reinforcement for RCC work",
    unit: "kg",
    rate: "65.00",
    category: "Steel",
  },
  {
    id: "6",
    code: "SSR-006",
    description: "Plastering with cement mortar 1:4",
    unit: "sqm",
    rate: "125.00",
    category: "Finishing",
  },
];

const categories = ["All", "Earthwork", "Concrete", "Masonry", "Steel", "Finishing"];

export default function SSRDatabase() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  const filteredItems = mockSSRItems.filter((item) => {
    const matchesSearch =
      item.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === "All" || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-3xl font-semibold">SSR Database</h1>
          <p className="text-sm text-muted-foreground mt-2">
            Standard Schedule of Rates for construction items
          </p>
        </div>
        <Button data-testid="button-add-ssr">
          <Plus className="h-4 w-4 mr-2" />
          Add SSR Item
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-lg">Categories</CardTitle>
            <CardDescription>Filter by category</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {categories.map((category) => (
              <Button
                key={category}
                variant={selectedCategory === category ? "secondary" : "ghost"}
                className="w-full justify-start"
                onClick={() => setSelectedCategory(category)}
                data-testid={`button-category-${category.toLowerCase()}`}
              >
                {category}
              </Button>
            ))}
          </CardContent>
        </Card>

        <div className="lg:col-span-3 space-y-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by code or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
              data-testid="input-search"
            />
          </div>

          <div className="border rounded-md">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-32">Code</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead className="w-24">Unit</TableHead>
                  <TableHead className="w-32 text-right">Rate (₹)</TableHead>
                  <TableHead className="w-32">Category</TableHead>
                  <TableHead className="w-24 text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredItems.length > 0 ? (
                  filteredItems.map((item) => (
                    <TableRow key={item.id} className="hover-elevate">
                      <TableCell className="font-mono text-sm">{item.code}</TableCell>
                      <TableCell className="text-sm">{item.description}</TableCell>
                      <TableCell className="text-sm">{item.unit}</TableCell>
                      <TableCell className="text-right font-mono text-sm">
                        {item.rate}
                      </TableCell>
                      <TableCell>
                        <Badge variant="secondary">{item.category}</Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex gap-2 justify-end">
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => console.log('Edit:', item.id)}
                            data-testid={`button-edit-${item.id}`}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => console.log('Delete:', item.id)}
                            data-testid={`button-delete-${item.id}`}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                      No items found
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>
    </div>
  );
}
