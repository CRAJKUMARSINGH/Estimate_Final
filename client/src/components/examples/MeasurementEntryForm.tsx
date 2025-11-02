import { useState } from "react";
import MeasurementEntryForm, { MeasurementRow } from "../MeasurementEntryForm";

export default function MeasurementEntryFormExample() {
  const [rows, setRows] = useState<MeasurementRow[]>([]);

  const handleAddRow = (row: MeasurementRow) => {
    setRows([...rows, row]);
    console.log("Row added:", row);
  };

  return (
    <div className="space-y-4">
      <MeasurementEntryForm onAddRow={handleAddRow} />
      {rows.length > 0 && (
        <div className="text-sm text-muted-foreground">
          Added {rows.length} row{rows.length !== 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}
