import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Save, Download, ArrowLeft } from "lucide-react";
import { Link } from "wouter";
import { EstimateSheetTabs } from "@/components/EstimateSheetTabs";
import { ExcelTable } from "@/components/ExcelTable";
import { ProjectMetadataForm } from "@/components/ProjectMetadataForm";
import { SSRItemSelector } from "@/components/SSRItemSelector";

export default function EstimateEditor() {
  const [showSSRSelector, setShowSSRSelector] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div className="flex items-center gap-4">
          <Link href="/estimates">
            <Button variant="ghost" size="icon" data-testid="button-back">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <div>
            <h1 className="text-2xl font-semibold">Highway Construction Phase 1</h1>
            <p className="text-sm text-muted-foreground mt-1">
              EST-2025-001 • Mumbai, Maharashtra
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" data-testid="button-save">
            <Save className="h-4 w-4 mr-2" />
            Save
          </Button>
          <Button data-testid="button-download">
            <Download className="h-4 w-4 mr-2" />
            Download Excel
          </Button>
        </div>
      </div>

      <ProjectMetadataForm />

      <EstimateSheetTabs />

      <ExcelTable />

      <SSRItemSelector
        open={showSSRSelector}
        onOpenChange={setShowSSRSelector}
        onSelect={(item) => console.log('Selected SSR item:', item)}
      />
    </div>
  );
}
