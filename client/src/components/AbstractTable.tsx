import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from "@/components/ui/card";

export interface AbstractItem {
  id: string;
  itemNo: string;
  description: string;
  quantity: number;
  unit: string;
  rate: number;
  amount: number;
}

interface AbstractTableProps {
  items: AbstractItem[];
  title: string;
}

export default function AbstractTable({ items, title }: AbstractTableProps) {
  const subtotal = items.reduce((sum, item) => sum + item.amount, 0);
  const contingency = subtotal * 0.03;
  const supervision = subtotal * 0.02;
  const grandTotal = subtotal + contingency + supervision;

  return (
    <Card className="overflow-hidden">
      <div className="bg-muted/50 px-6 py-4 border-b">
        <h3 className="text-lg font-semibold">{title}</h3>
      </div>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/30">
              <TableHead className="w-16 text-xs font-semibold uppercase tracking-wide">
                Item
              </TableHead>
              <TableHead className="min-w-[300px] text-xs font-semibold uppercase tracking-wide">
                Description
              </TableHead>
              <TableHead className="w-28 text-right text-xs font-semibold uppercase tracking-wide">
                Quantity
              </TableHead>
              <TableHead className="w-20 text-xs font-semibold uppercase tracking-wide">
                Unit
              </TableHead>
              <TableHead className="w-32 text-right text-xs font-semibold uppercase tracking-wide">
                Rate (₹)
              </TableHead>
              <TableHead className="w-36 text-right text-xs font-semibold uppercase tracking-wide">
                Amount (₹)
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items.map((item, index) => (
              <TableRow
                key={item.id}
                className={index % 2 === 0 ? "bg-background" : "bg-muted/20"}
                data-testid={`row-abstract-${item.id}`}
              >
                <TableCell className="font-medium">{item.itemNo}</TableCell>
                <TableCell>{item.description}</TableCell>
                <TableCell className="text-right font-mono">
                  {item.quantity.toFixed(3)}
                </TableCell>
                <TableCell>{item.unit}</TableCell>
                <TableCell className="text-right font-mono">
                  {item.rate.toFixed(2)}
                </TableCell>
                <TableCell className="text-right font-mono font-medium">
                  {item.amount.toFixed(2)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="border-t bg-muted/20">
        <div className="px-6 py-4 space-y-2">
          <div className="flex justify-between text-sm">
            <span className="font-medium">Sub-total:</span>
            <span className="font-mono font-semibold" data-testid="text-subtotal">
              ₹ {subtotal.toFixed(2)}
            </span>
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Add: Contingency (3%):</span>
            <span className="font-mono">₹ {contingency.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Add: Work Supervision (2%):</span>
            <span className="font-mono">₹ {supervision.toFixed(2)}</span>
          </div>
          <div className="pt-2 border-t flex justify-between text-base font-semibold">
            <span>Grand Total:</span>
            <span className="font-mono text-lg" data-testid="text-abstract-grand-total">
              ₹ {grandTotal.toFixed(2)}
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
}
