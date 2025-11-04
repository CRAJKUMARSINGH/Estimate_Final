import XLSX from 'xlsx';
import fs from 'fs';

// Create a test Excel file with multiple sheets
const workbook = XLSX.utils.book_new();

// Sheet 1: Cost Abstract
const costData = [
  ['S.No', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount'],
  [1, 'Excavation in all types of soil', 'cum', 100, 150, 15000],
  [2, 'Plain Cement Concrete 1:4:8', 'cum', 50, 4500, 225000],
  [3, 'Reinforced Cement Concrete M20', 'cum', 25, 6800, 170000],
  [4, 'Brick work in cement mortar 1:6', 'sqm', 200, 580, 116000],
  [5, 'Steel reinforcement for RCC work', 'kg', 1000, 65, 65000]
];

const costSheet = XLSX.utils.aoa_to_sheet(costData);
XLSX.utils.book_append_sheet(workbook, costSheet, 'ABSTRACT OF COST PART-1');

// Sheet 2: Measurements
const measurementData = [
  ['S.No', 'Description', 'Length', 'Breadth', 'Height', 'Quantity', 'Unit'],
  [1, 'Foundation excavation', 20, 1.5, 3, 90, 'cum'],
  [2, 'Footing concrete', 18, 1.2, 0.3, 6.48, 'cum'],
  [3, 'Column concrete', 0.3, 0.3, 3, 2.7, 'cum'],
  [4, 'Beam concrete', 0.25, 0.4, 15, 1.5, 'cum']
];

const measurementSheet = XLSX.utils.aoa_to_sheet(measurementData);
XLSX.utils.book_append_sheet(workbook, measurementSheet, 'MEASUREMENTS PART-1');

// Sheet 3: Project Info
const projectData = [
  ['Field', 'Value'],
  ['Project Name', 'Test Commercial Complex'],
  ['Location', 'Test City'],
  ['Engineer', 'Test Engineer'],
  ['Date', new Date().toLocaleDateString()],
  ['Status', 'Draft']
];

const projectSheet = XLSX.utils.aoa_to_sheet(projectData);
XLSX.utils.book_append_sheet(workbook, projectSheet, 'PROJECT INFO');

// Write the file
XLSX.writeFile(workbook, 'test-estimate.xlsx');
console.log('Test Excel file created: test-estimate.xlsx');