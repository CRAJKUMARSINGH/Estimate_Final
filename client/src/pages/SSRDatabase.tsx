import { useState } from "react";
import { Database, Search, Filter } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import SSRImportDialog, { ImportedSSRItem } from "@/components/SSRImportDialog";

export default function SSRDatabase() {
  const [searchQuery, setSearchQuery] = useState("");
  const [category, setCategory] = useState("all");

  const [ssrItems, setSSRItems] = useState([
    {
      code: "2.1.1",
      description: "Earth work excavation in foundation by manual means",
      category: "Earth Work",
      unit: "cum",
      rate: 245.50,
      effectiveDate: "Jan 2024",
    },
    {
      code: "2.1.2",
      description: "Earth work excavation by mechanical means",
      category: "Earth Work",
      unit: "cum",
      rate: 185.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "3.2.1",
      description: "Cement concrete 1:2:4 using 20mm aggregate",
      category: "Concrete Work",
      unit: "cum",
      rate: 4850.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "4.1.1",
      description: "Brick work in superstructure using common burnt clay bricks",
      category: "Masonry Work",
      unit: "cum",
      rate: 5200.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "5.3.2",
      description: "12mm thick cement plaster 1:4",
      category: "Plastering",
      unit: "sqm",
      rate: 125.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "6.2.1",
      description: "Painting with acrylic emulsion paint",
      category: "Painting",
      unit: "sqm",
      rate: 45.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "7.1.3",
      description: "PVC pipes 110mm dia for drainage",
      category: "Plumbing",
      unit: "m",
      rate: 285.00,
      effectiveDate: "Jan 2024",
    },
  ]);

  const handleImportComplete = (items: ImportedSSRItem[]) => {
    const newItems = items.map((item, index) => ({
      ...item,
      category: item.category || "Imported Items",
      effectiveDate: item.effectiveDate || "Jan 2024",
    }));
    
    setSSRItems([...ssrItems, ...newItems]);
    console.log(`Imported ${items.length} SSR items`);
  };

  const filteredItems = ssrItems.filter((item) => {
    const matchesSearch =
      item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.code.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = category === "all" || item.category === category;
    return matchesSearch && matchesCategory;
  });

  const categories = Array.from(new Set(ssrItems.map((item) => item.category)));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Database className="h-6 w-6 text-primary" />
          <div>
            <h1 className="text-2xl font-semibold">SSR Database</h1>
            <p className="text-sm text-muted-foreground">
              Standard Schedule of Rates - Browse and search
            </p>
          </div>
        </div>
        <SSRImportDialog onImportComplete={handleImportComplete} />
      </div>

      <Card className="p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by code or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
              data-testid="input-ssr-database-search"
            />
          </div>
          <div className="flex gap-2">
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-[200px]" data-testid="select-category">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
        <div className="mt-2 text-xs text-muted-foreground">
          Showing {filteredItems.length} of {ssrItems.length} items
        </div>
      </Card>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader className="bg-muted/50">
              <TableRow>
                <TableHead className="w-24 text-xs font-semibold uppercase tracking-wide">
                  Code
                </TableHead>
                <TableHead className="min-w-[350px] text-xs font-semibold uppercase tracking-wide">
                  Description
                </TableHead>
                <TableHead className="w-32 text-xs font-semibold uppercase tracking-wide">
                  Category
                </TableHead>
                <TableHead className="w-20 text-xs font-semibold uppercase tracking-wide">
                  Unit
                </TableHead>
                <TableHead className="w-32 text-right text-xs font-semibold uppercase tracking-wide">
                  Rate (₹)
                </TableHead>
                <TableHead className="w-28 text-xs font-semibold uppercase tracking-wide">
                  Effective
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredItems.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={6}
                    className="h-32 text-center text-muted-foreground"
                  >
                    No items found
                  </TableCell>
                </TableRow>
              ) : (
                filteredItems.map((item, index) => (
                  <TableRow
                    key={item.code}
                    className={index % 2 === 0 ? "bg-background" : "bg-muted/20"}
                    data-testid={`row-ssr-item-${item.code}`}
                  >
                    <TableCell className="font-mono text-sm font-medium">
                      {item.code}
                    </TableCell>
                    <TableCell className="text-sm">{item.description}</TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {item.category}
                    </TableCell>
                    <TableCell className="text-sm">{item.unit}</TableCell>
                    <TableCell className="text-right font-mono font-medium">
                      {item.rate.toFixed(2)}
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {item.effectiveDate}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </Card>
    </div>
  );
}
