import { Calculator } from "lucide-react";
import AbstractTable, { AbstractItem } from "@/components/AbstractTable";
import SSRSearchDialog, { SSRItem } from "@/components/SSRSearchDialog";

interface AbstractPageProps {
  title: string;
}

export default function AbstractPage({ title }: AbstractPageProps) {
  const abstractItems: AbstractItem[] = [
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
  ];

  const handleSelectSSR = (item: SSRItem) => {
    console.log("Selected SSR item:", item);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Calculator className="h-6 w-6 text-primary" />
          <div>
            <h1 className="text-2xl font-semibold">{title}</h1>
            <p className="text-sm text-muted-foreground">
              Auto-calculated cost summary from measurement sheets
            </p>
          </div>
        </div>
        <SSRSearchDialog ssrItems={ssrItems} onSelectItem={handleSelectSSR} />
      </div>

      <AbstractTable
        items={abstractItems}
        title="Commercial Complex - Panchayat Samiti Girwa"
      />

      <div className="text-sm text-muted-foreground bg-muted/30 rounded-md p-4 border">
        <p className="font-medium mb-2">Calculation Info:</p>
        <ul className="space-y-1 text-xs">
          <li>• Quantities are automatically summed from measurement sheets</li>
          <li>• Rates are applied from SSR database</li>
          <li>• Amounts are calculated as Quantity × Rate</li>
          <li>• All changes in measurement sheets update this abstract in real-time</li>
        </ul>
      </div>
    </div>
  );
}
