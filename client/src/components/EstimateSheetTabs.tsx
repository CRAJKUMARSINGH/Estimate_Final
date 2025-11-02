import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface Sheet {
  id: string;
  name: string;
  type: "info" | "cost" | "measurement" | "other";
}

const mockSheets: Sheet[] = [
  { id: "1", name: "Project Info", type: "info" },
  { id: "2", name: "ABSTRACT OF COST PART-1", type: "cost" },
  { id: "3", name: "MEASUREMENTS PART-1", type: "measurement" },
  { id: "4", name: "ABSTRACT OF COST PART-2", type: "cost" },
  { id: "5", name: "MEASUREMENTS PART-2", type: "measurement" },
  { id: "6", name: "GENERAL ABSTRACT", type: "other" },
];

export function EstimateSheetTabs() {
  const [activeSheet, setActiveSheet] = useState("1");

  const handleAddPart = () => {
    console.log('Add new part clicked');
  };

  return (
    <div className="space-y-4">
      <Tabs value={activeSheet} onValueChange={setActiveSheet} className="w-full">
        <div className="flex items-center gap-4 overflow-x-auto border-b pb-2">
          <TabsList className="h-auto bg-transparent p-0 gap-2 flex-wrap">
            {mockSheets.map((sheet) => (
              <TabsTrigger
                key={sheet.id}
                value={sheet.id}
                className="px-4 py-2 rounded-t-lg min-w-32 data-[state=active]:bg-card"
                data-testid={`tab-${sheet.id}`}
              >
                {sheet.name}
              </TabsTrigger>
            ))}
          </TabsList>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleAddPart}
            className="ml-auto"
            data-testid="button-add-part"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Part
          </Button>
        </div>

        {mockSheets.map((sheet) => (
          <TabsContent key={sheet.id} value={sheet.id} className="mt-4">
            <div className="border rounded-md p-4 bg-card">
              <p className="text-sm text-muted-foreground">
                Content for {sheet.name} will be displayed here
              </p>
            </div>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
