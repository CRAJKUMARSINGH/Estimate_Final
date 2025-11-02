import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export interface MeasurementItem {
  id: string;
  itemNo: string;
  description: string;
  quantity: number;
  length: number;
  breadth: number;
  height: number;
  unit: string;
  total: number;
}

interface MeasurementTableProps {
  items: MeasurementItem[];
  onDeleteItem: (id: string) => void;
}

export default function MeasurementTable({
  items,
  onDeleteItem,
}: MeasurementTableProps) {
  const grandTotal = items.reduce((sum, item) => sum + item.total, 0);

  return (
    <div className="border rounded-md overflow-hidden">
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead className="w-20 text-xs font-semibold uppercase tracking-wide">
                S.No.
              </TableHead>
              <TableHead className="min-w-[250px] text-xs font-semibold uppercase tracking-wide">
                Particulars
              </TableHead>
              <TableHead className="w-20 text-right text-xs font-semibold uppercase tracking-wide">
                Nos.
              </TableHead>
              <TableHead className="w-24 text-right text-xs font-semibold uppercase tracking-wide">
                Length
              </TableHead>
              <TableHead className="w-24 text-right text-xs font-semibold uppercase tracking-wide">
                Breadth
              </TableHead>
              <TableHead className="w-24 text-right text-xs font-semibold uppercase tracking-wide">
                Height
              </TableHead>
              <TableHead className="w-28 text-right text-xs font-semibold uppercase tracking-wide">
                Qty.
              </TableHead>
              <TableHead className="w-24 text-xs font-semibold uppercase tracking-wide">
                Units
              </TableHead>
              <TableHead className="w-16"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={9}
                  className="h-32 text-center text-muted-foreground"
                >
                  No measurements added yet
                </TableCell>
              </TableRow>
            ) : (
              <>
                {items.map((item, index) => (
                  <TableRow
                    key={item.id}
                    className={index % 2 === 0 ? "bg-background" : "bg-muted/20"}
                    data-testid={`row-measurement-${item.id}`}
                  >
                    <TableCell className="font-medium text-center">{item.itemNo}</TableCell>
                    <TableCell>{item.description}</TableCell>
                    <TableCell className="text-right font-mono">
                      {item.quantity.toFixed(0)}
                    </TableCell>
                    <TableCell className="text-right font-mono">
                      {item.length > 0 ? item.length.toFixed(2) : "-"}
                    </TableCell>
                    <TableCell className="text-right font-mono">
                      {item.breadth > 0 ? item.breadth.toFixed(2) : "-"}
                    </TableCell>
                    <TableCell className="text-right font-mono">
                      {item.height > 0 ? item.height.toFixed(2) : "-"}
                    </TableCell>
                    <TableCell className="text-right font-mono font-medium">
                      {item.total.toFixed(2)}
                    </TableCell>
                    <TableCell className="text-center">{item.unit}</TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => onDeleteItem(item.id)}
                        data-testid={`button-delete-${item.id}`}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
                <TableRow className="bg-muted font-semibold">
                  <TableCell colSpan={6} className="text-right uppercase tracking-wide">
                    TOTAL =
                  </TableCell>
                  <TableCell className="text-right font-mono" data-testid="text-grand-total">
                    {grandTotal.toFixed(2)}
                  </TableCell>
                  <TableCell className="text-center">{items[0]?.unit || ""}</TableCell>
                  <TableCell></TableCell>
                </TableRow>
              </>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
