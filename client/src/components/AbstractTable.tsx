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
  
  // Calculate electrification @ 7% on Civil Work (assuming first item is Civil Work)
  const civilWorkAmount = items.find(item => item.description.includes("Civil Work"))?.amount || 0;
  const electrification = civilWorkAmount * 0.07;
  
  const totalAfterElectrification = subtotal + electrification;
  
  // Add Prorata Charges @ 13%
  const prorataCharges = totalAfterElectrification * 0.13;
  
  const grandTotal = totalAfterElectrification + prorataCharges;

  return (
    <Card className="overflow-hidden">
      <div className="bg-muted/50 px-6 py-4 border-b text-center">
        <h3 className="text-base font-semibold uppercase">{title}</h3>
        <p className="text-xs text-muted-foreground mt-1">ABSTRACT OF COST</p>
      </div>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/30">
              <TableHead className="w-20 text-xs font-semibold uppercase tracking-wide text-center">
                S.No.
              </TableHead>
              <TableHead className="min-w-[300px] text-xs font-semibold uppercase tracking-wide">
                Particulars
              </TableHead>
              <TableHead className="w-28 text-right text-xs font-semibold uppercase tracking-wide">
                Quantity
              </TableHead>
              <TableHead className="w-24 text-xs font-semibold uppercase tracking-wide text-center">
                Unit
              </TableHead>
              <TableHead className="w-32 text-right text-xs font-semibold uppercase tracking-wide">
                Rate
              </TableHead>
              <TableHead className="w-36 text-right text-xs font-semibold uppercase tracking-wide">
                Amount
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
                <TableCell className="font-medium text-center">{item.itemNo}</TableCell>
                <TableCell>{item.description}</TableCell>
                <TableCell className="text-right font-mono">
                  {item.quantity.toFixed(2)}
                </TableCell>
                <TableCell className="text-center">{item.unit}</TableCell>
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
          <div className="flex justify-between text-sm border-b pb-2">
            <span className="font-medium">TOTAL Rs.</span>
            <span className="font-mono font-semibold" data-testid="text-subtotal">
              {subtotal.toFixed(2)}
            </span>
          </div>
          {civilWorkAmount > 0 && (
            <div className="flex justify-between text-sm">
              <div>
                <div className="font-medium">Add @ 7 % for Electrification On Civil Work Part 'A'</div>
                <div className="text-xs text-muted-foreground">i.e. on Rs. {civilWorkAmount.toFixed(2)}</div>
              </div>
              <div className="text-right">
                <div className="font-mono">Rs. {electrification.toFixed(2)}</div>
                <div className="font-mono font-semibold mt-1 pt-1 border-t">TOTAL Rs. {totalAfterElectrification.toFixed(2)}</div>
              </div>
            </div>
          )}
          <div className="flex justify-between text-sm pt-2 border-t">
            <span className="font-medium">Add Prorata Charges @ 13%</span>
            <span className="font-mono">{prorataCharges.toFixed(2)}</span>
          </div>
          <div className="pt-2 border-t flex justify-between text-base font-semibold">
            <span className="uppercase">GRAND TOTAL Rs.</span>
            <span className="font-mono text-lg" data-testid="text-abstract-grand-total">
              {grandTotal.toFixed(2)}
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
}
