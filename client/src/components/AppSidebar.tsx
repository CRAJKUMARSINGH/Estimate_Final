import { useState } from "react";
import {
  LayoutDashboard,
  FileText,
  Calculator,
  Database,
  FileOutput,
  ChevronDown,
  Ruler,
  Droplet,
  Trees,
  Zap,
  Building,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuSubButton,
  SidebarHeader,
} from "@/components/ui/sidebar";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import ProjectSelector from "./ProjectSelector";

interface AppSidebarProps {
  activePage: string;
  onNavigate: (page: string) => void;
}

export default function AppSidebar({ activePage, onNavigate }: AppSidebarProps) {
  const [measurementOpen, setMeasurementOpen] = useState(true);
  const [abstractOpen, setAbstractOpen] = useState(false);
  const [selectedProject, setSelectedProject] = useState("1");

  const projects = [
    {
      id: "1",
      name: "Commercial Complex - Panchayat Samiti Girwa",
      location: "Girwa, Udaipur",
    },
    {
      id: "2",
      name: "Community Hall Construction",
      location: "Mavli, Udaipur",
    },
  ];

  const measurementSheets = [
    { id: "civil", label: "Civil Work", icon: Building },
    { id: "sanitary", label: "Sanitary Work", icon: Droplet },
    { id: "landscape", label: "Landscape Work", icon: Trees },
    { id: "electrical", label: "Electrical Work", icon: Zap },
  ];

  const abstracts = [
    { id: "general", label: "General Abstract" },
    { id: "ssr-based", label: "SSR-Based Abstract" },
    { id: "cost", label: "Abstract of Cost" },
  ];

  return (
    <Sidebar>
      <SidebarHeader className="p-4">
        <div className="space-y-2">
          <div className="flex items-center gap-2 mb-4">
            <Ruler className="h-5 w-5 text-primary" />
            <span className="font-semibold text-lg">CE Estimator</span>
          </div>
          <ProjectSelector
            projects={projects}
            selectedProject={selectedProject}
            onProjectChange={setSelectedProject}
          />
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  onClick={() => onNavigate("dashboard")}
                  isActive={activePage === "dashboard"}
                  data-testid="nav-dashboard"
                >
                  <LayoutDashboard className="h-4 w-4" />
                  <span>Dashboard</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel className="text-xs font-medium uppercase tracking-wider">
            Measurements
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <Collapsible
                open={measurementOpen}
                onOpenChange={setMeasurementOpen}
              >
                <SidebarMenuItem>
                  <CollapsibleTrigger asChild>
                    <SidebarMenuButton data-testid="nav-measurement-sheets">
                      <FileText className="h-4 w-4" />
                      <span>Measurement Sheets</span>
                      <ChevronDown
                        className={`ml-auto h-4 w-4 transition-transform ${
                          measurementOpen ? "rotate-180" : ""
                        }`}
                      />
                    </SidebarMenuButton>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <SidebarMenuSub>
                      {measurementSheets.map((sheet) => (
                        <SidebarMenuSubItem key={sheet.id}>
                          <SidebarMenuSubButton
                            onClick={() => onNavigate(`measurement-${sheet.id}`)}
                            isActive={activePage === `measurement-${sheet.id}`}
                            data-testid={`nav-${sheet.id}`}
                          >
                            <sheet.icon className="h-4 w-4" />
                            <span>{sheet.label}</span>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      ))}
                    </SidebarMenuSub>
                  </CollapsibleContent>
                </SidebarMenuItem>
              </Collapsible>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel className="text-xs font-medium uppercase tracking-wider">
            Abstracts
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <Collapsible open={abstractOpen} onOpenChange={setAbstractOpen}>
                <SidebarMenuItem>
                  <CollapsibleTrigger asChild>
                    <SidebarMenuButton data-testid="nav-abstracts">
                      <Calculator className="h-4 w-4" />
                      <span>Cost Abstracts</span>
                      <ChevronDown
                        className={`ml-auto h-4 w-4 transition-transform ${
                          abstractOpen ? "rotate-180" : ""
                        }`}
                      />
                    </SidebarMenuButton>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <SidebarMenuSub>
                      {abstracts.map((abstract) => (
                        <SidebarMenuSubItem key={abstract.id}>
                          <SidebarMenuSubButton
                            onClick={() => onNavigate(`abstract-${abstract.id}`)}
                            isActive={activePage === `abstract-${abstract.id}`}
                            data-testid={`nav-${abstract.id}`}
                          >
                            <span>{abstract.label}</span>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      ))}
                    </SidebarMenuSub>
                  </CollapsibleContent>
                </SidebarMenuItem>
              </Collapsible>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  onClick={() => onNavigate("ssr-database")}
                  isActive={activePage === "ssr-database"}
                  data-testid="nav-ssr-database"
                >
                  <Database className="h-4 w-4" />
                  <span>SSR Database</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton
                  onClick={() => onNavigate("reports")}
                  isActive={activePage === "reports"}
                  data-testid="nav-reports"
                >
                  <FileOutput className="h-4 w-4" />
                  <span>Reports & Export</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
