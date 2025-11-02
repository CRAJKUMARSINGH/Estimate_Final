import AbstractTable, { AbstractItem } from "../AbstractTable";

export default function AbstractTableExample() {
  const items: AbstractItem[] = [
    {
      id: "1",
      itemNo: "A",
      description: "Civil Work - Earth excavation, concrete foundation, brick masonry",
      quantity: 51.6,
      unit: "cum",
      rate: 4850.0,
      amount: 250260.0,
    },
    {
      id: "2",
      itemNo: "B",
      description: "Sanitary Work - Plumbing, fixtures, drainage system",
      quantity: 1,
      unit: "LS",
      rate: 125000.0,
      amount: 125000.0,
    },
    {
      id: "3",
      itemNo: "C",
      description: "Electrical Work - Wiring, switches, distribution board",
      quantity: 1,
      unit: "LS",
      rate: 85000.0,
      amount: 85000.0,
    },
  ];

  return (
    <AbstractTable items={items} title="General Abstract - Commercial Complex" />
  );
}
