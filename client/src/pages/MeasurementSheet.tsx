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
      description: "Earth work excavation in foundation",
      quantity: 1,
      length: 10.5,
      breadth: 2.0,
      height: 1.5,
      unit: "cum",
      total: 31.5,
    },
    {
      id: "2",
      itemNo: "2",
      description: "Cement concrete 1:2:4 in foundation",
      quantity: 1,
      length: 10.5,
      breadth: 2.0,
      height: 0.3,
      unit: "cum",
      total: 6.3,
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
