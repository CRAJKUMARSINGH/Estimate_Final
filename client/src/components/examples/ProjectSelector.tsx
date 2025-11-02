import { useState } from "react";
import ProjectSelector from "../ProjectSelector";

export default function ProjectSelectorExample() {
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
    {
      id: "3",
      name: "School Building Renovation",
      location: "Bhinder, Udaipur",
    },
  ];

  return (
    <div className="w-80">
      <ProjectSelector
        projects={projects}
        selectedProject={selectedProject}
        onProjectChange={setSelectedProject}
      />
    </div>
  );
}
