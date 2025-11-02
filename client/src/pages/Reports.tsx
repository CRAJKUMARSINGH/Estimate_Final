import { FileText, Download, Printer, FileSpreadsheet } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function Reports() {
  const handleExport = (format: string) => {
    console.log(`Exporting as ${format}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <FileText className="h-6 w-6 text-primary" />
        <div>
          <h1 className="text-2xl font-semibold">Reports & Export</h1>
          <p className="text-sm text-muted-foreground">
            Generate and export estimation reports
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-primary/10 p-3 text-primary">
              <FileSpreadsheet className="h-6 w-6" />
            </div>
            <div>
              <h3 className="font-semibold">Excel Export</h3>
              <p className="text-xs text-muted-foreground">
                Download as .xlsx file
              </p>
            </div>
          </div>
          <Button
            className="w-full"
            onClick={() => handleExport("excel")}
            data-testid="button-export-excel"
          >
            <Download className="h-4 w-4 mr-2" />
            Export to Excel
          </Button>
        </Card>

        <Card className="p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-destructive/10 p-3 text-destructive">
              <FileText className="h-6 w-6" />
            </div>
            <div>
              <h3 className="font-semibold">PDF Export</h3>
              <p className="text-xs text-muted-foreground">
                Download as PDF file
              </p>
            </div>
          </div>
          <Button
            className="w-full"
            variant="outline"
            onClick={() => handleExport("pdf")}
            data-testid="button-export-pdf"
          >
            <Download className="h-4 w-4 mr-2" />
            Export to PDF
          </Button>
        </Card>

        <Card className="p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-accent p-3">
              <Printer className="h-6 w-6" />
            </div>
            <div>
              <h3 className="font-semibold">Print</h3>
              <p className="text-xs text-muted-foreground">
                Print formatted report
              </p>
            </div>
          </div>
          <Button
            className="w-full"
            variant="outline"
            onClick={() => window.print()}
            data-testid="button-print"
          >
            <Printer className="h-4 w-4 mr-2" />
            Print Report
          </Button>
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Report Preview</h3>
        <div className="border-2 border-dashed rounded-lg p-8 text-center text-muted-foreground bg-muted/20">
          <FileText className="h-12 w-12 mx-auto mb-3 opacity-50" />
          <p className="font-medium">Report preview will appear here</p>
          <p className="text-sm mt-1">
            Select a project and format to generate preview
          </p>
        </div>
      </Card>

      <Card className="p-6 bg-muted/30">
        <h4 className="font-semibold mb-3">Export Options</h4>
        <div className="space-y-2 text-sm">
          <div className="flex items-start gap-2">
            <div className="h-5 w-5 rounded bg-primary/20 flex items-center justify-center text-xs font-medium text-primary mt-0.5">
              1
            </div>
            <div>
              <p className="font-medium">Measurement Sheets</p>
              <p className="text-xs text-muted-foreground">
                Includes all component-wise measurements with calculations
              </p>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <div className="h-5 w-5 rounded bg-primary/20 flex items-center justify-center text-xs font-medium text-primary mt-0.5">
              2
            </div>
            <div>
              <p className="font-medium">General Abstract</p>
              <p className="text-xs text-muted-foreground">
                Component-wise cost summary
              </p>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <div className="h-5 w-5 rounded bg-primary/20 flex items-center justify-center text-xs font-medium text-primary mt-0.5">
              3
            </div>
            <div>
              <p className="font-medium">Abstract of Cost</p>
              <p className="text-xs text-muted-foreground">
                Final cost breakdown with contingency and supervision charges
              </p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
