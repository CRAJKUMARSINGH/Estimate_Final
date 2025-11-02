import { useState } from "react";
import { Search, Plus } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export interface SSRItem {
  code: string;
  description: string;
  unit: string;
  rate: number;
  effectiveDate: string;
}

interface SSRSearchDialogProps {
  ssrItems: SSRItem[];
  onSelectItem: (item: SSRItem) => void;
}

export default function SSRSearchDialog({
  ssrItems,
  onSelectItem,
}: SSRSearchDialogProps) {
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredItems = ssrItems.filter(
    (item) =>
      item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSelect = (item: SSRItem) => {
    onSelectItem(item);
    setOpen(false);
    setSearchQuery("");
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" data-testid="button-open-ssr-search">
          <Search className="h-4 w-4 mr-2" />
          Search SSR Database
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle>SSR Database - Standard Schedule of Rates</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by code or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
              data-testid="input-ssr-search"
            />
          </div>

          <div className="border rounded-md overflow-hidden max-h-[50vh] overflow-y-auto">
            <Table>
              <TableHeader className="sticky top-0 bg-muted/50">
                <TableRow>
                  <TableHead className="w-24 text-xs font-semibold uppercase tracking-wide">
                    Code
                  </TableHead>
                  <TableHead className="min-w-[300px] text-xs font-semibold uppercase tracking-wide">
                    Description
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
                  <TableHead className="w-20"></TableHead>
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
                      className={
                        index % 2 === 0 ? "bg-background" : "bg-muted/20"
                      }
                      data-testid={`row-ssr-${item.code}`}
                    >
                      <TableCell className="font-mono text-sm">
                        {item.code}
                      </TableCell>
                      <TableCell className="text-sm">{item.description}</TableCell>
                      <TableCell className="text-sm">{item.unit}</TableCell>
                      <TableCell className="text-right font-mono">
                        {item.rate.toFixed(2)}
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {item.effectiveDate}
                      </TableCell>
                      <TableCell>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleSelect(item)}
                          data-testid={`button-select-${item.code}`}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>

          <div className="text-xs text-muted-foreground">
            Showing {filteredItems.length} of {ssrItems.length} items
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
