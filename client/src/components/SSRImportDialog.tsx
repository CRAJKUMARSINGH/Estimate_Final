import { useState } from "react";
import { Upload, FileSpreadsheet, Check, AlertCircle } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import * as XLSX from 'xlsx';

export interface ImportedSSRItem {
  code: string;
  description: string;
  unit: string;
  rate: number;
  category?: string;
  effectiveDate?: string;
}

interface SSRImportDialogProps {
  onImportComplete: (items: ImportedSSRItem[]) => void;
}

export default function SSRImportDialog({ onImportComplete }: SSRImportDialogProps) {
  const [open, setOpen] = useState(false);
  const [importing, setImporting] = useState(false);
  const [importStatus, setImportStatus] = useState<{
    success: boolean;
    count: number;
    message: string;
  } | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setImporting(true);
    setImportStatus(null);

    try {
      const data = await file.arrayBuffer();
      const workbook = XLSX.read(data);
      
      // Read first sheet
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      
      // Convert to JSON
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 }) as any[][];
      
      // Parse SSR data - assuming format: Code | Description | Unit | Rate
      // Skip header row
      const importedItems: ImportedSSRItem[] = [];
      
      for (let i = 1; i < jsonData.length; i++) {
        const row = jsonData[i];
        
        // Skip empty rows
        if (!row || row.length === 0 || !row[0]) continue;
        
        // Try to parse the row - flexible format
        const code = String(row[0] || '').trim();
        const description = String(row[1] || '').trim();
        const unit = String(row[2] || 'Cum').trim();
        const rate = parseFloat(String(row[3] || '0').replace(/[^0-9.]/g, ''));
        const category = row[4] ? String(row[4]).trim() : undefined;
        const effectiveDate = row[5] ? String(row[5]).trim() : 'Jan 2024';
        
        if (code && description && !isNaN(rate)) {
          importedItems.push({
            code,
            description,
            unit,
            rate,
            category,
            effectiveDate,
          });
        }
      }
      
      if (importedItems.length > 0) {
        onImportComplete(importedItems);
        setImportStatus({
          success: true,
          count: importedItems.length,
          message: `Successfully imported ${importedItems.length} SSR items`,
        });
        
        // Auto-close after 2 seconds
        setTimeout(() => {
          setOpen(false);
          setImportStatus(null);
        }, 2000);
      } else {
        setImportStatus({
          success: false,
          count: 0,
          message: 'No valid SSR items found in the Excel file. Please check the format.',
        });
      }
    } catch (error) {
      console.error('Import error:', error);
      setImportStatus({
        success: false,
        count: 0,
        message: `Failed to import: ${error instanceof Error ? error.message : 'Unknown error'}`,
      });
    } finally {
      setImporting(false);
      // Reset file input
      event.target.value = '';
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" data-testid="button-import-ssr">
          <Upload className="h-4 w-4 mr-2" />
          Import Excel SSR
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Import SSR from Excel</DialogTitle>
          <DialogDescription>
            Upload an Excel file containing Standard Schedule of Rates (SSR) data
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="excel-file">Excel File (.xlsx, .xls)</Label>
            <div className="flex items-center gap-2">
              <Input
                id="excel-file"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileUpload}
                disabled={importing}
                data-testid="input-excel-file"
                className="cursor-pointer"
              />
              <FileSpreadsheet className="h-5 w-5 text-muted-foreground shrink-0" />
            </div>
          </div>

          {importing && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <div className="animate-spin h-4 w-4 border-2 border-primary border-t-transparent rounded-full" />
              <span>Importing SSR data...</span>
            </div>
          )}

          {importStatus && (
            <div
              className={`flex items-start gap-2 p-3 rounded-md ${
                importStatus.success
                  ? 'bg-green-500/10 text-green-700 dark:text-green-400'
                  : 'bg-destructive/10 text-destructive'
              }`}
              data-testid="text-import-status"
            >
              {importStatus.success ? (
                <Check className="h-5 w-5 shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
              )}
              <div className="text-sm">
                <p className="font-medium">{importStatus.message}</p>
                {importStatus.success && importStatus.count > 0 && (
                  <p className="text-xs mt-1 opacity-80">
                    {importStatus.count} items added to SSR database
                  </p>
                )}
              </div>
            </div>
          )}

          <div className="bg-muted/30 rounded-md p-3 text-xs space-y-2">
            <p className="font-medium">Expected Excel Format:</p>
            <div className="space-y-1 text-muted-foreground">
              <p>Column A: Code (e.g., 2.1.1)</p>
              <p>Column B: Description</p>
              <p>Column C: Unit (e.g., Cum, Sqm, RM)</p>
              <p>Column D: Rate (numeric value)</p>
              <p>Column E: Category (optional)</p>
              <p>Column F: Effective Date (optional)</p>
            </div>
            <p className="text-muted-foreground mt-2">
              First row should contain headers and will be skipped.
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
