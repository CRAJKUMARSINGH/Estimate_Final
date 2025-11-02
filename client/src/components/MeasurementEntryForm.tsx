import { useState } from "react";
import { Plus, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card } from "@/components/ui/card";

export interface MeasurementRow {
  itemNo: string;
  description: string;
  quantity: string;
  length: string;
  breadth: string;
  height: string;
  unit: string;
}

interface MeasurementEntryFormProps {
  onAddRow: (row: MeasurementRow) => void;
}

const units = ["RM", "Cum", "Sqm", "Nos", "Kg", "Ton", "Ltr", "LS"];

export default function MeasurementEntryForm({
  onAddRow,
}: MeasurementEntryFormProps) {
  const [formData, setFormData] = useState<MeasurementRow>({
    itemNo: "",
    description: "",
    quantity: "1",
    length: "",
    breadth: "",
    height: "",
    unit: "RM",
  });

  const calculateTotal = () => {
    const qty = parseFloat(formData.quantity) || 0;
    const l = parseFloat(formData.length) || 1;
    const b = parseFloat(formData.breadth) || 1;
    const h = parseFloat(formData.height) || 1;
    return (qty * l * b * h).toFixed(3);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAddRow(formData);
    setFormData({
      itemNo: "",
      description: "",
      quantity: "1",
      length: "",
      breadth: "",
      height: "",
      unit: "RM",
    });
  };

  return (
    <Card className="p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
          <div className="space-y-2">
            <Label htmlFor="itemNo" className="text-xs font-medium uppercase tracking-wider">
              S.No.
            </Label>
            <Input
              id="itemNo"
              value={formData.itemNo}
              onChange={(e) =>
                setFormData({ ...formData, itemNo: e.target.value })
              }
              placeholder="1"
              required
              data-testid="input-item-no"
            />
          </div>

          <div className="md:col-span-2 space-y-2">
            <Label htmlFor="description" className="text-xs font-medium uppercase tracking-wider">
              Particulars
            </Label>
            <Input
              id="description"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              placeholder="Main walls 380 mm th.in Y Direction..."
              required
              data-testid="input-description"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="quantity" className="text-xs font-medium uppercase tracking-wider">
              Nos.
            </Label>
            <Input
              id="quantity"
              type="number"
              step="1"
              value={formData.quantity}
              onChange={(e) =>
                setFormData({ ...formData, quantity: e.target.value })
              }
              placeholder="1"
              className="text-right font-mono"
              data-testid="input-quantity"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="length" className="text-xs font-medium uppercase tracking-wider">
              Length (m)
            </Label>
            <Input
              id="length"
              type="number"
              step="0.01"
              value={formData.length}
              onChange={(e) =>
                setFormData({ ...formData, length: e.target.value })
              }
              placeholder="0.00"
              className="text-right font-mono"
              data-testid="input-length"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="breadth" className="text-xs font-medium uppercase tracking-wider">
              Breadth (m)
            </Label>
            <Input
              id="breadth"
              type="number"
              step="0.01"
              value={formData.breadth}
              onChange={(e) =>
                setFormData({ ...formData, breadth: e.target.value })
              }
              placeholder="0.00"
              className="text-right font-mono"
              data-testid="input-breadth"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
          <div className="space-y-2">
            <Label htmlFor="height" className="text-xs font-medium uppercase tracking-wider">
              Height (m)
            </Label>
            <Input
              id="height"
              type="number"
              step="0.01"
              value={formData.height}
              onChange={(e) =>
                setFormData({ ...formData, height: e.target.value })
              }
              placeholder="0.00"
              className="text-right font-mono"
              data-testid="input-height"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="unit" className="text-xs font-medium uppercase tracking-wider">
              Units
            </Label>
            <Select
              value={formData.unit}
              onValueChange={(value) =>
                setFormData({ ...formData, unit: value })
              }
            >
              <SelectTrigger id="unit" data-testid="select-unit">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {units.map((unit) => (
                  <SelectItem key={unit} value={unit}>
                    {unit.toUpperCase()}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label className="text-xs font-medium uppercase tracking-wider">
              Qty.
            </Label>
            <Input
              value={calculateTotal()}
              readOnly
              className="bg-muted text-right font-mono font-medium"
              data-testid="text-total"
            />
          </div>

          <div className="md:col-span-3 flex items-end gap-2">
            <Button type="submit" className="flex-1" data-testid="button-add-row">
              <Plus className="h-4 w-4 mr-2" />
              Add Row
            </Button>
            <Button type="button" variant="outline" data-testid="button-save">
              <Save className="h-4 w-4 mr-2" />
              Save
            </Button>
          </div>
        </div>
      </form>
    </Card>
  );
}
