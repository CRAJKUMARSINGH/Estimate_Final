import SSRSearchDialog, { SSRItem } from "../SSRSearchDialog";

export default function SSRSearchDialogExample() {
  const ssrItems: SSRItem[] = [
    {
      code: "2.1.1",
      description: "Earth work excavation in foundation by manual means",
      unit: "cum",
      rate: 245.50,
      effectiveDate: "Jan 2024",
    },
    {
      code: "2.1.2",
      description: "Earth work excavation by mechanical means",
      unit: "cum",
      rate: 185.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "3.2.1",
      description: "Cement concrete 1:2:4 using 20mm aggregate",
      unit: "cum",
      rate: 4850.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "4.1.1",
      description: "Brick work in superstructure using common burnt clay bricks",
      unit: "cum",
      rate: 5200.00,
      effectiveDate: "Jan 2024",
    },
    {
      code: "5.3.2",
      description: "12mm thick cement plaster 1:4",
      unit: "sqm",
      rate: 125.00,
      effectiveDate: "Jan 2024",
    },
  ];

  const handleSelect = (item: SSRItem) => {
    console.log("Selected SSR item:", item);
  };

  return <SSRSearchDialog ssrItems={ssrItems} onSelectItem={handleSelect} />;
}
