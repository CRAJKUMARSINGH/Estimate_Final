import { useState } from "react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import AppSidebar from "@/components/AppSidebar";
import ThemeToggle from "@/components/ThemeToggle";
import Dashboard from "@/pages/Dashboard";
import MeasurementSheet from "@/pages/MeasurementSheet";
import AbstractPage from "@/pages/AbstractPage";
import SSRDatabase from "@/pages/SSRDatabase";
import Reports from "@/pages/Reports";
import { Building, Droplet, Trees, Zap } from "lucide-react";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const style = {
    "--sidebar-width": "20rem",
    "--sidebar-width-icon": "4rem",
  };

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <Dashboard />;
      case "measurement-civil":
        return <MeasurementSheet title="Civil Work" icon={Building} />;
      case "measurement-sanitary":
        return <MeasurementSheet title="Sanitary Work" icon={Droplet} />;
      case "measurement-landscape":
        return <MeasurementSheet title="Landscape Work" icon={Trees} />;
      case "measurement-electrical":
        return <MeasurementSheet title="Electrical Work" icon={Zap} />;
      case "abstract-general":
        return <AbstractPage title="General Abstract" />;
      case "abstract-ssr-based":
        return <AbstractPage title="SSR-Based Abstract" />;
      case "abstract-cost":
        return <AbstractPage title="Abstract of Cost" />;
      case "ssr-database":
        return <SSRDatabase />;
      case "reports":
        return <Reports />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <SidebarProvider style={style as React.CSSProperties}>
          <div className="flex h-screen w-full overflow-hidden">
            <AppSidebar activePage={activePage} onNavigate={setActivePage} />
            <div className="flex flex-col flex-1 overflow-hidden">
              <header className="flex items-center justify-between gap-4 px-6 py-3 border-b bg-background">
                <SidebarTrigger data-testid="button-sidebar-toggle" />
                <ThemeToggle />
              </header>
              <main className="flex-1 overflow-y-auto p-8">
                <div className="max-w-7xl mx-auto">{renderPage()}</div>
              </main>
            </div>
          </div>
        </SidebarProvider>
        <Toaster />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
