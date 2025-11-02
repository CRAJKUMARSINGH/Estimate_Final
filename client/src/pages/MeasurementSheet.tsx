import { useState } from "react";
import { Building } from "lucide-react";
import MeasurementEntryForm, { MeasurementRow } from "@/components/MeasurementEntryForm";
import MeasurementTable, { MeasurementItem } from "@/components/MeasurementTable";

interface MeasurementSheetProps {
  title: string;
  icon: React.ComponentType<{ className?: string }>;
}

export default function MeasurementSheet({
  title,
  icon: Icon = Building,
}: MeasurementSheetProps) {
  const [items, setItems] = useState<MeasurementItem[]>([
    {
      id: "1",
      itemNo: "1",
      description: "Main walls 380 mm th.in Y Direction - Litigant Shed",
      quantity: 4,
      length: 8.16,
      breadth: 0,
      height: 0,
      unit: "RM",
      total: 32.64,
    },
    {
      id: "2",
      itemNo: "2",
      description: "Main walls 380 mm th.in Y Direction - Stamp",
      quantity: 4,
      length: 10.67,
      breadth: 0,
      height: 0,
      unit: "RM",
      total: 42.68,
    },
    {
      id: "3",
      itemNo: "3",
      description: "Earth work in excavation in foundation trenches - Main walls 380mm thick",
      quantity: 1,
      length: 453.68,
      breadth: 1.20,
      height: 1.20,
      unit: "Cum",
      total: 653.30,
    },
  ]);

  const handleAddRow = (row: MeasurementRow) => {
    const total =
      (parseFloat(row.quantity) || 0) *
      (parseFloat(row.length) || 1) *
      (parseFloat(row.breadth) || 1) *
      (parseFloat(row.height) || 1);

    const newItem: MeasurementItem = {
      id: Date.now().toString(),
      itemNo: row.itemNo,
      description: row.description,
      quantity: parseFloat(row.quantity) || 0,
      length: parseFloat(row.length) || 0,
      breadth: parseFloat(row.breadth) || 0,
      height: parseFloat(row.height) || 0,
      unit: row.unit,
      total,
    };

    setItems([...items, newItem]);
  };

  const handleDeleteItem = (id: string) => {
    setItems(items.filter((item) => item.id !== id));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Icon className="h-6 w-6 text-primary" />
        <div>
          <h1 className="text-2xl font-semibold">{title}</h1>
          <p className="text-sm text-muted-foreground">
            Add and manage measurement entries
          </p>
        </div>
      </div>

      <MeasurementEntryForm onAddRow={handleAddRow} />
      <MeasurementTable items={items} onDeleteItem={handleDeleteItem} />
    </div>
  );
}
