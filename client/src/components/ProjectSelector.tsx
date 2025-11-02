import { useState } from "react";
import { Check, ChevronsUpDown, FolderOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";

interface Project {
  id: string;
  name: string;
  location: string;
}

interface ProjectSelectorProps {
  projects: Project[];
  selectedProject: string;
  onProjectChange: (projectId: string) => void;
}

export default function ProjectSelector({
  projects,
  selectedProject,
  onProjectChange,
}: ProjectSelectorProps) {
  const [open, setOpen] = useState(false);

  const currentProject = projects.find((p) => p.id === selectedProject);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between"
          data-testid="button-project-selector"
        >
          <div className="flex items-center gap-2 truncate">
            <FolderOpen className="h-4 w-4 shrink-0" />
            <span className="truncate">
              {currentProject ? currentProject.name : "Select project..."}
            </span>
          </div>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[300px] p-0">
        <Command>
          <CommandInput placeholder="Search projects..." data-testid="input-project-search" />
          <CommandList>
            <CommandEmpty>No project found.</CommandEmpty>
            <CommandGroup>
              {projects.map((project) => (
                <CommandItem
                  key={project.id}
                  value={project.id}
                  onSelect={() => {
                    onProjectChange(project.id);
                    setOpen(false);
                  }}
                  data-testid={`project-${project.id}`}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      selectedProject === project.id
                        ? "opacity-100"
                        : "opacity-0"
                    )}
                  />
                  <div className="flex flex-col">
                    <span className="text-sm font-medium">{project.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {project.location}
                    </span>
                  </div>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
