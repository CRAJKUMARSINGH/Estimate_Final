import { useState } from "react";
import { SidebarProvider } from "@/components/ui/sidebar";
import AppSidebar from "../AppSidebar";

export default function AppSidebarExample() {
  const [activePage, setActivePage] = useState("dashboard");

  const style = {
    "--sidebar-width": "20rem",
    "--sidebar-width-icon": "4rem",
  };

  return (
    <SidebarProvider style={style as React.CSSProperties}>
      <div className="flex h-screen w-full">
        <AppSidebar activePage={activePage} onNavigate={setActivePage} />
        <main className="flex-1 p-6">
          <div className="text-sm text-muted-foreground">
            Active page: {activePage}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}
