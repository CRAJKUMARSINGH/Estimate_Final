# EstimationPro - Web-Based Construction Cost Estimation System

A comprehensive web application that replaces traditional Excel-based construction estimation workflows with a modern, collaborative, and powerful platform.

## 🏗️ Features

### Core Functionality
- **Dynamic Excel Import System** - Seamlessly import existing Excel estimates with automatic sheet mapping
- **Real-time Calculations** - Automatic cost calculations with live updates as you edit
- **Interactive Editing** - Click-to-edit any field with undo/redo functionality
- **Multi-format Export** - Export to PDF, Excel, HTML, and CSV formats
- **SSR Database Management** - Comprehensive Standard Schedule of Rates management

### Advanced Features
- **Drag-and-Drop Import** - Simply drag Excel files onto the import area
- **Auto-detection** - Automatically detects sheet types based on naming patterns
- **Live Dashboard** - Real-time overview of projects, metrics, and recent activity
- **Collaborative Interface** - Modern UI with smooth interactions and animations
- **Data Validation** - Built-in validation and error prevention
- **Export History** - Track and re-download previous exports

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No server requirements - runs entirely in the browser

### Installation
1. Download or clone the project files
2. Open `index.html` in a web browser
3. Start using the application immediately

### First Steps
1. **Import Excel File**: Click "Import Excel" button and upload your existing estimate
2. **Navigate Dashboard**: Use the top navigation to switch between views
3. **Edit Estimates**: Click on any estimate to view and edit details
4. **Export Results**: Use the export button to generate reports in your preferred format

## 📊 System Architecture

### File Structure
```
EstimationPro/
├── index.html          # Main application interface
├── app.js             # Core application logic
├── user-guide.html    # Comprehensive user documentation
├── README.md          # This file
└── resources/         # Static assets (optional)
```

### Technology Stack
- **Frontend**: HTML5, CSS3 (Tailwind CSS), JavaScript (ES6+)
- **Libraries**: 
  - Alpine.js - Reactive framework
  - XLSX.js - Excel file handling
  - jsPDF - PDF generation
  - Font Awesome - Icons
- **Charts**: Canvas-based custom charts
- **Storage**: Browser localStorage for persistence

### Key Components

#### Excel Import System
- **File Handling**: Supports .xlsx, .xls, .xlsm formats
- **Sheet Detection**: Auto-maps sheets based on naming patterns
- **Data Processing**: Preserves formulas and hierarchical relationships
- **Error Handling**: Comprehensive validation and user feedback

#### Calculation Engine
- **Real-time Updates**: Instant calculations as you type
- **Hierarchical Summation**: Part totals roll up to general abstract
- **Formula Preservation**: Maintains Excel-like calculation logic
- **Performance**: Optimized for large datasets

#### Export System
- **PDF Export**: Professional formatted reports
- **Excel Export**: Preserves formulas and structure
- **HTML Export**: Web-ready reports
- **CSV Export**: Data analysis format

## 🎯 Usage Guide

### Importing Excel Files
1. Click the "Import Excel" button
2. Select your Excel file or drag-and-drop onto the import area
3. The system automatically detects and maps sheets
4. Review the imported data and make adjustments as needed

### Managing Estimates
- **Create**: Click "New Estimate" to start from scratch
- **Edit**: Click on any estimate to open the detailed view
- **Duplicate**: Use the copy icon to create duplicates
- **Delete**: Use the trash icon (with confirmation)

### Working with Parts and Items
- **Add Parts**: Use "Add Part" button in estimate detail view
- **Add Items**: Use "Add Item" button within each part
- **Edit Values**: Click on any field to edit inline
- **Delete Items**: Use the trash icon next to each item

### Exporting Results
1. Click the "Export" button
2. Choose your preferred format (PDF, Excel, HTML, CSV)
3. Enter a filename
4. The export begins automatically

## 🔧 Configuration

### Customization Options
The application can be customized by modifying the `app.js` file:

```javascript
// Customize default SSR items
ssrItems: [
    { id: 1, code: 'CW-001', description: 'Your description', unit: 'Cum', rate: 100.00, category: 'Civil Work' }
],

// Customize export settings
exportFormat: 'pdf',
exportFilename: 'MyEstimate',

// Add custom calculation formulas
updateCalculations() {
    // Your custom logic here
}
```

### Styling
The application uses Tailwind CSS for styling. Customize colors and layouts by modifying the HTML classes or adding custom CSS.

## 📈 Best Practices

### Excel Import
- Use consistent naming conventions for sheets
- Include headers in the first row
- Avoid merged cells in data areas
- Use standard units (RM, Cum, Sqm, Nos, Kg, Ton)

### Data Management
- Regularly update SSR rates
- Validate quantities before finalizing
- Use descriptive names for estimates and parts
- Backup important estimates by exporting

### Performance
- For large datasets, consider splitting into multiple estimates
- Use search and filter features to navigate quickly
- Regular cleanup of old estimates improves performance

## 🔍 Troubleshooting

### Common Issues

**Excel Import Fails**
- Check file format (.xlsx, .xls, .xlsm)
- Ensure file is not password protected
- Verify sheet naming conventions
- Check browser console for error messages

**Calculations Not Updating**
- Refresh the page and try again
- Check for empty or invalid cells
- Verify rate entries are numeric
- Ensure quantities are properly formatted

**Export Problems**
- Clear browser cache
- Try different export format
- Check file size limits
- Disable browser extensions temporarily

### Browser Compatibility
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 📚 Documentation

- **User Guide**: Comprehensive guide available at `user-guide.html`
- **API Reference**: Inline documentation in `app.js`
- **Examples**: Sample data included in the application

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the user guide at `user-guide.html`
- Review the troubleshooting section
- Open an issue in the repository
- Contact the development team

## 🔄 Updates

The application includes automatic update checking. When new versions are available, you'll be notified with update instructions.

## 🎉 Acknowledgments

- Inspired by traditional Excel-based estimation workflows
- Built with modern web technologies
- Designed for construction professionals
- Optimized for performance and usability

---

**EstimationPro** - Transforming construction cost estimation with modern web technology.