import { useState } from "react";
import MeasurementTable, { MeasurementItem } from "../MeasurementTable";

export default function MeasurementTableExample() {
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
    {
      id: "3",
      itemNo: "3",
      description: "Brick work in superstructure",
      quantity: 2,
      length: 10.0,
      breadth: 3.0,
      height: 0.23,
      unit: "cum",
      total: 13.8,
    },
  ]);

  const handleDelete = (id: string) => {
    setItems(items.filter((item) => item.id !== id));
    console.log("Deleted item:", id);
  };

  return <MeasurementTable items={items} onDeleteItem={handleDelete} />;
}
