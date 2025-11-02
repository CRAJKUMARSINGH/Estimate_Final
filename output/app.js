// EstimationPro Application Logic
document.addEventListener('alpine:init', () => {
    Alpine.data('estimationApp', () => ({
        // State Management
        currentView: 'dashboard',
        estimates: [],
        ssrItems: [],
        exportHistory: [],
        recentActivity: [],
        
        // Modal States
        showImportModal: false,
        showExportModal: false,
        showEstimateModal: false,
        showAddSSRModal: false,
        
        // Form States
        searchQuery: '',
        filterType: '',
        ssrSearchQuery: '',
        exportFormat: 'pdf',
        exportFilename: '',
        isDragging: false,
        importProgress: 0,
        importStatus: '',
        
        // Current Estimate
        currentEstimate: null,
        estimateTab: 'general',
        
        // Initialize Application
        init() {
            this.loadSampleData();
            this.initializeCharts();
            this.initializeCorrections();
            this.watchTabChange();
        },
        
        // Initialize Corrections System
        initializeCorrections() {
            this.correctionIssues = [];
            this.findText = '';
            this.replaceText = '';
        },
        
        // Watch for tab changes to run validation
        watchTabChange() {
            this.$watch('estimateTab', (value) => {
                if (value === 'corrections') {
                    this.validateEstimate();
                }
            });
        },
        
        // Minor Corrections Functions
        validateEstimate() {
            this.correctionIssues = [];
            let issueId = 1;
            
            if (!this.currentEstimate || !this.currentEstimate.parts) {
                this.correctionIssues.push({
                    id: issueId++,
                    type: 'error',
                    message: 'No estimate data found',
                    location: 'Estimate Structure'
                });
                return;
            }
            
            this.currentEstimate.parts.forEach((part, partIndex) => {
                // Check for missing descriptions
                if (part.abstractItems) {
                    part.abstractItems.forEach((item, itemIndex) => {
                        if (!item.description || item.description.trim() === '') {
                            this.correctionIssues.push({
                                id: issueId++,
                                type: 'error',
                                message: 'Missing description',
                                location: `Part ${partIndex + 1}, Item ${itemIndex + 1}`,
                                partIndex: partIndex,
                                itemIndex: itemIndex,
                                field: 'description'
                            });
                        }
                        
                        if (item.quantity === 0) {
                            this.correctionIssues.push({
                                id: issueId++,
                                type: 'warning',
                                message: 'Zero quantity',
                                location: `Part ${partIndex + 1}, Item ${itemIndex + 1}`,
                                partIndex: partIndex,
                                itemIndex: itemIndex,
                                field: 'quantity'
                            });
                        }
                        
                        if (!item.unit || item.unit === '') {
                            this.correctionIssues.push({
                                id: issueId++,
                                type: 'warning',
                                message: 'Missing unit',
                                location: `Part ${partIndex + 1}, Item ${itemIndex + 1}`,
                                partIndex: partIndex,
                                itemIndex: itemIndex,
                                field: 'unit'
                            });
                        }
                        
                        if (item.rate === 0) {
                            this.correctionIssues.push({
                                id: issueId++,
                                type: 'warning',
                                message: 'Zero rate',
                                location: `Part ${partIndex + 1}, Item ${itemIndex + 1}`,
                                partIndex: partIndex,
                                itemIndex: itemIndex,
                                field: 'rate'
                            });
                        }
                    });
                }
            });
            
            if (this.correctionIssues.length === 0) {
                this.addActivity('fas fa-check', 'Estimate validation completed - no issues found');
            } else {
                this.addActivity('fas fa-exclamation-triangle', `Found ${this.correctionIssues.length} issues in estimate`);
            }
        },
        
        fixIssue(issue) {
            if (!this.currentEstimate || !this.currentEstimate.parts[issue.partIndex]) return;
            
            const part = this.currentEstimate.parts[issue.partIndex];
            const item = part.abstractItems[issue.itemIndex];
            
            switch (issue.field) {
                case 'description':
                    item.description = 'Fixed Description';
                    break;
                case 'quantity':
                    item.quantity = 1;
                    break;
                case 'unit':
                    item.unit = 'Cum';
                    break;
                case 'rate':
                    item.rate = 100;
                    break;
            }
            
            // Recalculate amount
            item.amount = item.quantity * item.rate;
            this.updateCalculations();
            
            // Remove the fixed issue
            this.correctionIssues = this.correctionIssues.filter(i => i.id !== issue.id);
            
            this.addActivity('fas fa-wrench', `Fixed: ${issue.message}`);
        },
        
        fixMissingDescriptions() {
            if (!this.currentEstimate || !this.currentEstimate.parts) return;
            
            let fixedCount = 0;
            this.currentEstimate.parts.forEach((part, partIndex) => {
                if (part.abstractItems) {
                    part.abstractItems.forEach((item, itemIndex) => {
                        if (!item.description || item.description.trim() === '') {
                            item.description = `Item ${partIndex + 1}-${itemIndex + 1}`;
                            fixedCount++;
                        }
                    });
                }
            });
            
            if (fixedCount > 0) {
                this.updateCalculations();
                this.validateEstimate();
                this.addActivity('fas fa-text-width', `Fixed ${fixedCount} missing descriptions`);
            }
        },
        
        fixZeroQuantities() {
            if (!this.currentEstimate || !this.currentEstimate.parts) return;
            
            let fixedCount = 0;
            this.currentEstimate.parts.forEach(part => {
                if (part.abstractItems) {
                    part.abstractItems.forEach(item => {
                        if (item.quantity === 0) {
                            item.quantity = 1;
                            item.amount = item.quantity * item.rate;
                            fixedCount++;
                        }
                    });
                }
            });
            
            if (fixedCount > 0) {
                this.updateCalculations();
                this.validateEstimate();
                this.addActivity('fas fa-calculator', `Fixed ${fixedCount} zero quantities`);
            }
        },
        
        fixMissingUnits() {
            if (!this.currentEstimate || !this.currentEstimate.parts) return;
            
            let fixedCount = 0;
            this.currentEstimate.parts.forEach(part => {
                if (part.abstractItems) {
                    part.abstractItems.forEach(item => {
                        if (!item.unit || item.unit === '') {
                            item.unit = 'Cum';
                            fixedCount++;
                        }
                    });
                }
            });
            
            if (fixedCount > 0) {
                this.validateEstimate();
                this.addActivity('fas fa-ruler', `Fixed ${fixedCount} missing units`);
            }
        },
        
        standardizeDescriptions() {
            if (!this.currentEstimate || !this.currentEstimate.parts) return;
            
            let fixedCount = 0;
            this.currentEstimate.parts.forEach(part => {
                if (part.abstractItems) {
                    part.abstractItems.forEach(item => {
                        if (item.description && item.description.length > 50) {
                            // Truncate very long descriptions
                            item.description = item.description.substring(0, 50) + '...';
                            fixedCount++;
                        }
                        
                        // Remove extra whitespace
                        item.description = item.description.trim().replace(/\s+/g, ' ');
                    });
                }
            });
            
            if (fixedCount > 0) {
                this.updateCalculations();
                this.validateEstimate();
                this.addActivity('fas fa-align-left', `Standardized ${fixedCount} descriptions`);
            }
        },
        
        bulkReplace() {
            if (!this.findText || !this.replaceText || !this.currentEstimate || !this.currentEstimate.parts) return;
            
            let replaceCount = 0;
            const findRegex = new RegExp(this.findText, 'gi');
            
            this.currentEstimate.parts.forEach(part => {
                if (part.abstractItems) {
                    part.abstractItems.forEach(item => {
                        const originalDescription = item.description;
                        item.description = item.description.replace(findRegex, this.replaceText);
                        
                        if (item.description !== originalDescription) {
                            replaceCount++;
                        }
                    });
                }
            });
            
            if (replaceCount > 0) {
                this.updateCalculations();
                this.validateEstimate();
                this.addActivity('fas fa-exchange-alt', `Replaced ${replaceCount} occurrences of "${this.findText}"`);
                
                // Clear the fields
                this.findText = '';
                this.replaceText = '';
            }
        },
        
        // Sample Data Loading
        loadSampleData() {
            // Load sample SSR items
            this.ssrItems = [
                { id: 1, code: 'CW-001', description: 'Earth work in excavation in foundation trenches or drains not exceeding 1.5 m in width or 10 sqm on plan including dressing of sides and ramming of bottoms', unit: 'Cum', rate: 245.50, category: 'Civil Work' },
                { id: 2, code: 'CW-002', description: 'Cement concrete 1:4:8 in foundation with 40mm down grade coarse aggregate', unit: 'Cum', rate: 4567.80, category: 'Civil Work' },
                { id: 3, code: 'SW-001', description: 'Providing and fixing PVC pipes for water supply', unit: 'RM', rate: 156.75, category: 'Sanitary Work' },
                { id: 4, code: 'EW-001', description: 'Providing and fixing conduit pipes for electrical wiring', unit: 'RM', rate: 89.25, category: 'Electrical Work' },
                { id: 5, code: 'LW-001', description: 'Planting and maintenance of ornamental plants', unit: 'Nos', rate: 45.30, category: 'Landscape Work' }
            ];
            
            // Load sample estimates
            this.estimates = [
                {
                    id: 1,
                    name: 'Commercial Complex Estimate',
                    description: 'Complete estimation for commercial building project',
                    type: 'civil',
                    createdDate: new Date('2024-01-15'),
                    totalAmount: 2847560,
                    parts: [
                        {
                            id: 'part_1',
                            name: 'Ground Floor',
                            measurementItems: [
                                { id: 'm1', description: 'Earth excavation', unit: 'Cum', quantity: 150 },
                                { id: 'm2', description: 'Concrete foundation', unit: 'Cum', quantity: 75 }
                            ],
                            abstractItems: [
                                { id: 'a1', description: 'Earth excavation', unit: 'Cum', quantity: 150, rate: 245.50, amount: 36825 },
                                { id: 'a2', description: 'Concrete foundation', unit: 'Cum', quantity: 75, rate: 4567.80, amount: 342585 }
                            ]
                        },
                        {
                            id: 'part_2',
                            name: 'First Floor',
                            measurementItems: [
                                { id: 'm3', description: 'Brick work', unit: 'Cum', quantity: 120 },
                                { id: 'm4', description: 'Plastering', unit: 'Sqm', quantity: 450 }
                            ],
                            abstractItems: [
                                { id: 'a3', description: 'Brick work', unit: 'Cum', quantity: 120, rate: 3456.20, amount: 414744 },
                                { id: 'a4', description: 'Plastering', unit: 'Sqm', quantity: 450, rate: 234.50, amount: 105525 }
                            ]
                        }
                    ]
                },
                {
                    id: 2,
                    name: 'Residential Building',
                    description: 'Estimation for residential construction project',
                    type: 'civil',
                    createdDate: new Date('2024-02-10'),
                    totalAmount: 1567890,
                    parts: [
                        {
                            id: 'part_3',
                            name: 'Foundation',
                            measurementItems: [
                                { id: 'm5', description: 'Excavation', unit: 'Cum', quantity: 100 },
                                { id: 'm6', description: 'Concrete', unit: 'Cum', quantity: 50 }
                            ],
                            abstractItems: [
                                { id: 'a5', description: 'Excavation', unit: 'Cum', quantity: 100, rate: 245.50, amount: 24550 },
                                { id: 'a6', description: 'Concrete', unit: 'Cum', quantity: 50, rate: 4567.80, amount: 228390 }
                            ]
                        }
                    ]
                }
            ];
            
            // Load sample recent activity
            this.recentActivity = [
                { id: 1, icon: 'fas fa-file-import', description: 'Imported Excel estimate: Commercial Complex', timestamp: '2 hours ago' },
                { id: 2, icon: 'fas fa-plus', description: 'Created new estimate: Residential Building', timestamp: '5 hours ago' },
                { id: 3, icon: 'fas fa-download', description: 'Exported estimate to PDF format', timestamp: '1 day ago' },
                { id: 4, icon: 'fas fa-edit', description: 'Updated SSR database with new rates', timestamp: '2 days ago' }
            ];
        },
        
        // Computed Properties
        get activeProjects() {
            return this.estimates.filter(e => e.parts && e.parts.length > 0).length;
        },
        
        get totalValue() {
            return this.estimates.reduce((sum, estimate) => sum + (estimate.totalAmount || 0), 0);
        },
        
        get filteredEstimates() {
            return this.estimates.filter(estimate => {
                const matchesSearch = estimate.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                                    estimate.description.toLowerCase().includes(this.searchQuery.toLowerCase());
                const matchesType = !this.filterType || estimate.type === this.filterType;
                return matchesSearch && matchesType;
            });
        },
        
        get filteredSSRItems() {
            return this.ssrItems.filter(item => 
                item.description.toLowerCase().includes(this.ssrSearchQuery.toLowerCase()) ||
                item.code.toLowerCase().includes(this.ssrSearchQuery.toLowerCase())
            );
        },
        
        // Utility Functions
        formatCurrency(amount) {
            return new Intl.NumberFormat('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(amount);
        },
        
        formatNumber(number) {
            return new Intl.NumberFormat('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(number);
        },
        
        formatDate(date) {
            return new Intl.DateTimeFormat('en-IN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            }).format(date);
        },
        
        getTypeBadge(type) {
            const badges = {
                'civil': 'bg-blue-100 text-blue-800',
                'sanitary': 'bg-green-100 text-green-800',
                'electrical': 'bg-yellow-100 text-yellow-800',
                'landscape': 'bg-purple-100 text-purple-800'
            };
            return badges[type] || 'bg-gray-100 text-gray-800';
        },
        
        getExportIcon(format) {
            const icons = {
                'pdf': 'fas fa-file-pdf',
                'excel': 'fas fa-file-excel',
                'html': 'fas fa-file-code',
                'csv': 'fas fa-file-csv'
            };
            return icons[format] || 'fas fa-file';
        },
        
        // Estimate Management
        createNewEstimate() {
            const newEstimate = {
                id: Date.now(),
                name: 'New Estimate',
                description: 'Description here',
                type: 'civil',
                createdDate: new Date(),
                totalAmount: 0,
                parts: []
            };
            this.estimates.unshift(newEstimate);
            this.openEstimate(newEstimate);
        },
        
        openEstimate(estimate) {
            this.currentEstimate = JSON.parse(JSON.stringify(estimate));
            this.estimateTab = 'general';
            this.showEstimateModal = true;
        },
        
        duplicateEstimate(estimate) {
            const duplicate = {
                ...JSON.parse(JSON.stringify(estimate)),
                id: Date.now(),
                name: estimate.name + ' (Copy)',
                createdDate: new Date()
            };
            this.estimates.unshift(duplicate);
            this.addActivity('fas fa-copy', `Duplicated estimate: ${estimate.name}`);
        },
        
        deleteEstimate(estimate) {
            if (confirm(`Are you sure you want to delete "${estimate.name}"?`)) {
                this.estimates = this.estimates.filter(e => e.id !== estimate.id);
                this.addActivity('fas fa-trash', `Deleted estimate: ${estimate.name}`);
            }
        },
        
        // Part Management
        addNewPart() {
            if (!this.currentEstimate) return;
            
            const newPart = {
                id: 'part_' + Date.now(),
                name: 'New Part ' + (this.currentEstimate.parts.length + 1),
                measurementItems: [],
                abstractItems: []
            };
            
            this.currentEstimate.parts.push(newPart);
            this.updateCalculations();
        },
        
        deletePart(part) {
            if (!this.currentEstimate) return;
            
            if (confirm(`Are you sure you want to delete "${part.name}" and all its items?`)) {
                this.currentEstimate.parts = this.currentEstimate.parts.filter(p => p.id !== part.id);
                this.updateCalculations();
                this.addActivity('fas fa-trash', `Deleted part: ${part.name}`);
            }
        },
        
        getPartTotal(part) {
            if (!part || !part.abstractItems) return 0;
            return part.abstractItems.reduce((sum, item) => sum + (item.amount || 0), 0);
        },
        
        getTotalItems() {
            if (!this.currentEstimate || !this.currentEstimate.parts) return 0;
            return this.currentEstimate.parts.reduce((sum, part) => sum + (part.abstractItems?.length || 0), 0);
        },
        
        // Item Management
        addItemToPart(part) {
            const newMeasurementItem = {
                id: 'm' + Date.now(),
                description: 'New Item',
                unit: 'Cum',
                quantity: 0
            };
            
            const newAbstractItem = {
                id: 'a' + Date.now(),
                description: 'New Item',
                unit: 'Cum',
                quantity: 0,
                rate: 0,
                amount: 0
            };
            
            part.measurementItems.push(newMeasurementItem);
            part.abstractItems.push(newAbstractItem);
            this.updateCalculations();
        },
        
        deleteMeasurementItem(part, item) {
            part.measurementItems = part.measurementItems.filter(i => i.id !== item.id);
            this.updateCalculations();
        },
        
        deleteAbstractItem(part, item) {
            part.abstractItems = part.abstractItems.filter(i => i.id !== item.id);
            this.updateCalculations();
        },
        
        // Calculation Engine
        updateCalculations() {
            if (!this.currentEstimate) return;
            
            // Update abstract item amounts
            this.currentEstimate.parts.forEach(part => {
                part.abstractItems.forEach(item => {
                    item.amount = (item.quantity || 0) * (item.rate || 0);
                });
            });
            
            // Update total amount
            this.currentEstimate.totalAmount = this.currentEstimate.parts.reduce((sum, part) => {
                return sum + this.getPartTotal(part);
            }, 0);
            
            // Update the main estimates array
            const index = this.estimates.findIndex(e => e.id === this.currentEstimate.id);
            if (index !== -1) {
                this.estimates[index] = JSON.parse(JSON.stringify(this.currentEstimate));
            }
        },
        
        // Excel Import/Export
        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                this.importExcelFile(file);
            }
        },
        
        handleFileDrop(event) {
            this.isDragging = false;
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                if (file.type.includes('sheet') || file.name.match(/\.(xlsx|xls|xlsm)$/i)) {
                    this.importExcelFile(file);
                }
            }
        },
        
        importExcelFile(file) {
            this.importProgress = 0;
            this.importStatus = 'Reading file...';
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    this.importStatus = 'Processing data...';
                    this.importProgress = 30;
                    
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array', cellFormula: true, cellStyles: true });
                    
                    this.importProgress = 60;
                    this.importStatus = 'Analyzing sheets...';
                    
                    // Process the workbook
                    const result = this.processExcelWorkbook(workbook);
                    
                    if (result.success) {
                        this.importProgress = 100;
                        this.importStatus = 'Import completed successfully!';
                        
                        // Add the imported estimate to the list
                        this.estimates.unshift(result.estimate);
                        
                        setTimeout(() => {
                            this.showImportModal = false;
                            this.importProgress = 0;
                            this.importStatus = '';
                            this.addActivity('fas fa-file-import', `Imported Excel file: ${file.name}`);
                        }, 1500);
                    } else {
                        throw new Error(result.error || 'Unknown import error');
                    }
                    
                } catch (error) {
                    console.error('Error importing Excel file:', error);
                    this.importStatus = `Error: ${error.message}`;
                    setTimeout(() => {
                        this.importProgress = 0;
                        this.importStatus = '';
                    }, 5000);
                }
            };
            
            reader.onerror = () => {
                this.importStatus = 'Error reading file. Please try again.';
                setTimeout(() => {
                    this.importProgress = 0;
                    this.importStatus = '';
                }, 3000);
            };
            
            reader.readAsArrayBuffer(file);
        },
        
        processExcelWorkbook(workbook) {
            try {
                const sheetNames = workbook.SheetNames;
                
                // Auto-detect sheet types based on naming patterns
                const generalAbstractSheet = sheetNames.find(name => 
                    name.toLowerCase().includes('general') && 
                    name.toLowerCase().includes('abstract')
                );
                
                const measurementSheets = sheetNames.filter(name => 
                    name.toLowerCase().includes('measurement')
                );
                
                const abstractSheets = sheetNames.filter(name => 
                    name.toLowerCase().includes('abstract') && 
                    !name.toLowerCase().includes('general')
                );
                
                // Create new estimate structure
                const newEstimate = {
                    id: Date.now(),
                    name: workbook.Props?.Title || 'Imported Estimate',
                    description: 'Imported from Excel',
                    type: 'civil',
                    createdDate: new Date(),
                    totalAmount: 0,
                    parts: []
                };
                
                // Process measurement and abstract sheets in pairs
                measurementSheets.forEach(measurementSheetName => {
                    const matchingAbstractSheet = this.findMatchingAbstractSheet(measurementSheetName, abstractSheets);
                    
                    if (matchingAbstractSheet) {
                        const measurementData = this.getSheetData(workbook, measurementSheetName);
                        const abstractData = this.getSheetData(workbook, matchingAbstractSheet);
                        
                        const part = this.createPartFromSheets(measurementSheetName, measurementData, abstractData);
                        if (part) {
                            newEstimate.parts.push(part);
                        }
                    }
                });
                
                // Process any remaining abstract sheets without measurement counterparts
                abstractSheets.forEach(sheetName => {
                    if (!newEstimate.parts.find(part => part.name === sheetName)) {
                        const abstractData = this.getSheetData(workbook, sheetName);
                        const part = this.createPartFromAbstractOnly(sheetName, abstractData);
                        if (part) {
                            newEstimate.parts.push(part);
                        }
                    }
                });
                
                // Calculate total amount
                newEstimate.totalAmount = newEstimate.parts.reduce((sum, part) => {
                    return sum + this.getPartTotal(part);
                }, 0);
                
                return {
                    success: true,
                    estimate: newEstimate
                };
                
            } catch (error) {
                console.error('Error processing workbook:', error);
                return {
                    success: false,
                    error: error.message
                };
            }
        },
        
        findMatchingAbstractSheet(measurementSheetName, abstractSheets) {
            // Extract part name from measurement sheet
            const partName = measurementSheetName
                .replace(/measurement/gi, '')
                .replace(/sheet/gi, '')
                .trim();
            
            // Find matching abstract sheet
            return abstractSheets.find(abstractSheet => 
                abstractSheet.toLowerCase().includes(partName.toLowerCase())
            ) || abstractSheets[0]; // Fallback to first abstract sheet
        },
        
        getSheetData(workbook, sheetName) {
            const sheet = workbook.Sheets[sheetName];
            if (!sheet) return [];
            
            // Convert sheet to JSON with headers
            return XLSX.utils.sheet_to_json(sheet, { 
                header: 1,
                defval: '',
                blankrows: false 
            });
        },
        
        createPartFromSheets(sheetName, measurementData, abstractData) {
            try {
                const partName = sheetName
                    .replace(/measurement/gi, '')
                    .replace(/sheet/gi, '')
                    .trim() || 'Part ' + (this.currentEstimate?.parts?.length + 1 || 1);
                
                const part = {
                    id: 'part_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
                    name: partName,
                    measurementItems: [],
                    abstractItems: []
                };
                
                // Process measurement data
                if (measurementData.length > 1) {
                    const headers = measurementData[0];
                    for (let i = 1; i < measurementData.length; i++) {
                        const row = measurementData[i];
                        if (row && row.length > 0 && row[0]) {
                            const item = {
                                id: 'm' + Date.now() + '_' + i,
                                description: row[0] || 'Item ' + i,
                                unit: row[1] || 'Cum',
                                quantity: this.parseNumericValue(row[2]) || 0
                            };
                            part.measurementItems.push(item);
                        }
                    }
                }
                
                // Process abstract data
                if (abstractData.length > 1) {
                    const headers = abstractData[0];
                    for (let i = 1; i < abstractData.length; i++) {
                        const row = abstractData[i];
                        if (row && row.length > 0 && row[0]) {
                            const item = {
                                id: 'a' + Date.now() + '_' + i,
                                description: row[0] || 'Item ' + i,
                                unit: row[1] || 'Cum',
                                quantity: this.parseNumericValue(row[2]) || 0,
                                rate: this.parseNumericValue(row[3]) || 0,
                                amount: 0
                            };
                            item.amount = item.quantity * item.rate;
                            part.abstractItems.push(item);
                        }
                    }
                }
                
                return part;
            } catch (error) {
                console.error('Error creating part from sheets:', error);
                return null;
            }
        },
        
        createPartFromAbstractOnly(sheetName, abstractData) {
            try {
                const partName = sheetName
                    .replace(/abstract/gi, '')
                    .replace(/of cost/gi, '')
                    .replace(/sheet/gi, '')
                    .trim() || 'Abstract Part';
                
                const part = {
                    id: 'part_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
                    name: partName,
                    measurementItems: [],
                    abstractItems: []
                };
                
                // Process abstract data only
                if (abstractData.length > 1) {
                    for (let i = 1; i < abstractData.length; i++) {
                        const row = abstractData[i];
                        if (row && row.length > 0 && row[0]) {
                            const item = {
                                id: 'a' + Date.now() + '_' + i,
                                description: row[0] || 'Item ' + i,
                                unit: row[1] || 'Cum',
                                quantity: this.parseNumericValue(row[2]) || 0,
                                rate: this.parseNumericValue(row[3]) || 0,
                                amount: 0
                            };
                            item.amount = item.quantity * item.rate;
                            part.abstractItems.push(item);
                            
                            // Create corresponding measurement item
                            const measurementItem = {
                                id: 'm' + Date.now() + '_' + i,
                                description: item.description,
                                unit: item.unit,
                                quantity: item.quantity
                            };
                            part.measurementItems.push(measurementItem);
                        }
                    }
                }
                
                return part;
            } catch (error) {
                console.error('Error creating part from abstract only:', error);
                return null;
            }
        },
        
        parseNumericValue(value) {
            if (typeof value === 'number') return value;
            if (typeof value === 'string') {
                // Remove currency symbols and commas, then parse
                const cleanValue = value.replace(/[₹$,]/g, '');
                const parsed = parseFloat(cleanValue);
                return isNaN(parsed) ? 0 : parsed;
            }
            return 0;
        },
        
        exportEstimate() {
            if (!this.exportFilename) {
                this.exportFilename = 'Estimate_' + new Date().toISOString().split('T')[0];
            }
            
            switch (this.exportFormat) {
                case 'pdf':
                    this.exportToPDF();
                    break;
                case 'excel':
                    this.exportToExcel();
                    break;
                case 'html':
                    this.exportToHTML();
                    break;
                case 'csv':
                    this.exportToCSV();
                    break;
            }
            
            this.showExportModal = false;
        },
        
        exportToPDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            
            // Add title
            doc.setFontSize(20);
            doc.text('Cost Estimate Report', 20, 30);
            
            // Add content
            doc.setFontSize(12);
            doc.text(`Project: ${this.exportFilename}`, 20, 50);
            doc.text(`Generated: ${new Date().toLocaleDateString()}`, 20, 65);
            
            // Add table data
            const tableData = [];
            if (this.currentEstimate && this.currentEstimate.parts) {
                this.currentEstimate.parts.forEach(part => {
                    tableData.push([part.name, '', '']);
                    if (part.abstractItems) {
                        part.abstractItems.forEach(item => {
                            tableData.push(['', item.description, `₹${this.formatCurrency(item.amount)}`]);
                        });
                    }
                    tableData.push(['', 'Part Total', `₹${this.formatCurrency(this.getPartTotal(part))}`]);
                    tableData.push(['', '', '']);
                });
            }
            
            doc.autoTable({
                startY: 80,
                head: [['Part', 'Description', 'Amount']],
                body: tableData
            });
            
            // Save the PDF
            doc.save(`${this.exportFilename}.pdf`);
            
            this.addToExportHistory('pdf', `${this.exportFilename}.pdf`);
            this.addActivity('fas fa-file-pdf', `Exported estimate to PDF: ${this.exportFilename}.pdf`);
        },
        
        exportToExcel() {
            const workbook = XLSX.utils.book_new();
            
            // Create General Abstract sheet
            const generalAbstractData = [
                ['Part Name', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount'],
                ...this.currentEstimate.parts.flatMap(part => [
                    [part.name, '', '', '', '', ''],
                    ...(part.abstractItems?.map(item => [
                        '',
                        item.description,
                        item.unit,
                        item.quantity,
                        item.rate,
                        item.amount
                    ]) || []),
                    ['', 'Part Total', '', '', '', this.getPartTotal(part)],
                    ['', '', '', '', '', ''] // Empty row between parts
                ])
            ];
            
            const generalAbstractSheet = XLSX.utils.aoa_to_sheet(generalAbstractData);
            XLSX.utils.book_append_sheet(workbook, generalAbstractSheet, 'General Abstract');
            
            // Create individual part sheets
            if (this.currentEstimate && this.currentEstimate.parts) {
                this.currentEstimate.parts.forEach(part => {
                    // Measurement sheet
                    if (part.measurementItems && part.measurementItems.length > 0) {
                        const measurementData = [
                            ['Description', 'Unit', 'Quantity'],
                            ...part.measurementItems.map(item => [
                                item.description,
                                item.unit,
                                item.quantity
                            ])
                        ];
                        
                        const measurementSheet = XLSX.utils.aoa_to_sheet(measurementData);
                        XLSX.utils.book_append_sheet(workbook, measurementSheet, `Measurement ${part.name}`);
                    }
                    
                    // Abstract sheet
                    if (part.abstractItems && part.abstractItems.length > 0) {
                        const abstractData = [
                            ['Description', 'Unit', 'Quantity', 'Rate', 'Amount'],
                            ...part.abstractItems.map(item => [
                                item.description,
                                item.unit,
                                item.quantity,
                                item.rate,
                                item.amount
                            ]),
                            ['', '', '', 'Total', this.getPartTotal(part)]
                        ];
                        
                        const abstractSheet = XLSX.utils.aoa_to_sheet(abstractData);
                        XLSX.utils.book_append_sheet(workbook, abstractSheet, `Abstract of Cost ${part.name}`);
                    }
                });
            }
            
            // Generate Excel file
            XLSX.writeFile(workbook, `${this.exportFilename}.xlsx`);
            
            this.addToExportHistory('excel', `${this.exportFilename}.xlsx`);
            this.addActivity('fas fa-file-excel', `Exported estimate to Excel: ${this.exportFilename}.xlsx`);
        },
        
        exportToHTML() {
            let htmlContent = `
                <!DOCTYPE html>
                <html>
                <head>
                    <title>${this.exportFilename}</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; }
                        .header { text-align: center; margin-bottom: 30px; }
                        .part { margin-bottom: 30px; }
                        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                        th { background-color: #f2f2f2; }
                        .total { font-weight: bold; background-color: #e8f5e8; }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>Cost Estimate Report</h1>
                        <p>Project: ${this.exportFilename}</p>
                        <p>Generated: ${new Date().toLocaleDateString()}</p>
                    </div>
            `;
            
            if (this.currentEstimate && this.currentEstimate.parts) {
                this.currentEstimate.parts.forEach(part => {
                    htmlContent += `
                        <div class="part">
                            <h2>${part.name}</h2>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Description</th>
                                        <th>Unit</th>
                                        <th>Quantity</th>
                                        <th>Rate</th>
                                        <th>Amount</th>
                                    </tr>
                                </thead>
                                <tbody>
                    `;
                    
                    if (part.abstractItems) {
                        part.abstractItems.forEach(item => {
                            htmlContent += `
                                <tr>
                                    <td>${item.description}</td>
                                    <td>${item.unit}</td>
                                    <td>${this.formatNumber(item.quantity)}</td>
                                    <td>₹${this.formatCurrency(item.rate)}</td>
                                    <td>₹${this.formatCurrency(item.amount)}</td>
                                </tr>
                            `;
                        });
                    }
                    
                    htmlContent += `
                                <tr class="total">
                                    <td colspan="4"><strong>Total</strong></td>
                                    <td><strong>₹${this.formatCurrency(this.getPartTotal(part))}</strong></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    `;
                });
            }
            
            htmlContent += '</body></html>';
            
            // Create and download HTML file
            const blob = new Blob([htmlContent], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${this.exportFilename}.html`;
            a.click();
            URL.revokeObjectURL(url);
            
            this.addToExportHistory('html', `${this.exportFilename}.html`);
            this.addActivity('fas fa-file-code', `Exported estimate to HTML: ${this.exportFilename}.html`);
        },
        
        exportToCSV() {
            let csvContent = 'Part,Description,Unit,Quantity,Rate,Amount\n';
            
            if (this.currentEstimate && this.currentEstimate.parts) {
                this.currentEstimate.parts.forEach(part => {
                    if (part.abstractItems) {
                        part.abstractItems.forEach(item => {
                            csvContent += `"${part.name}","${item.description}","${item.unit}",${item.quantity},${item.rate},${item.amount}\n`;
                        });
                    }
                    csvContent += `"${part.name}","Total","","","",${this.getPartTotal(part)}\n\n`;
                });
            }
            
            // Create and download CSV file
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${this.exportFilename}.csv`;
            a.click();
            URL.revokeObjectURL(url);
            
            this.addToExportHistory('csv', `${this.exportFilename}.csv`);
            this.addActivity('fas fa-file-csv', `Exported estimate to CSV: ${this.exportFilename}.csv`);
        },
        
        addToExportHistory(format, filename) {
            const exportRecord = {
                id: Date.now(),
                format: format,
                filename: filename,
                timestamp: new Date().toLocaleString(),
                data: this.currentEstimate
            };
            
            this.exportHistory.unshift(exportRecord);
            
            // Keep only last 10 exports
            if (this.exportHistory.length > 10) {
                this.exportHistory = this.exportHistory.slice(0, 10);
            }
        },
        
        downloadExport(exportRecord) {
            // Re-export the data
            this.currentEstimate = exportRecord.data;
            this.exportFormat = exportRecord.format;
            this.exportFilename = exportRecord.filename.replace(/\.(pdf|xlsx|html|csv)$/i, '');
            this.exportEstimate();
        },
        
        addActivity(icon, description) {
            const activity = {
                id: Date.now(),
                icon: icon,
                description: description,
                timestamp: new Date().toLocaleString()
            };
            
            this.recentActivity.unshift(activity);
            
            // Keep only last 20 activities
            if (this.recentActivity.length > 20) {
                this.recentActivity = this.recentActivity.slice(0, 20);
            }
        },
        
        // Chart Initialization
        initializeCharts() {
            // Wait for the DOM to be ready
            setTimeout(() => {
                this.createEstimatesByTypeChart();
                this.createCostDistributionChart();
            }, 100);
        },
        
        createEstimatesByTypeChart() {
            const canvas = document.getElementById('estimatesByTypeChart');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            
            // Calculate data
            const typeCount = {};
            this.estimates.forEach(estimate => {
                typeCount[estimate.type] = (typeCount[estimate.type] || 0) + 1;
            });
            
            // Chart data
            const labels = Object.keys(typeCount);
            const data = Object.values(typeCount);
            const colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6'];
            
            // Simple pie chart implementation
            this.drawPieChart(ctx, labels, data, colors, canvas.width, canvas.height);
        },
        
        createCostDistributionChart() {
            const canvas = document.getElementById('costDistributionChart');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            
            // Calculate data
            const costData = this.estimates.map(estimate => estimate.totalAmount);
            const labels = this.estimates.map(estimate => estimate.name);
            
            // Simple bar chart implementation
            this.drawBarChart(ctx, labels, costData, canvas.width, canvas.height);
        },
        
        drawPieChart(ctx, labels, data, colors, width, height) {
            const centerX = width / 2;
            const centerY = height / 2;
            const radius = Math.min(width, height) / 3;
            
            let total = data.reduce((sum, value) => sum + value, 0);
            let currentAngle = -Math.PI / 2;
            
            data.forEach((value, index) => {
                const sliceAngle = (value / total) * 2 * Math.PI;
                
                // Draw slice
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
                ctx.closePath();
                ctx.fillStyle = colors[index % colors.length];
                ctx.fill();
                
                // Draw label
                const labelAngle = currentAngle + sliceAngle / 2;
                const labelX = centerX + Math.cos(labelAngle) * (radius * 0.7);
                const labelY = centerY + Math.sin(labelAngle) * (radius * 0.7);
                
                ctx.fillStyle = '#000';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(`${labels[index]} (${value})`, labelX, labelY);
                
                currentAngle += sliceAngle;
            });
        },
        
        drawBarChart(ctx, labels, data, width, height) {
            const padding = 40;
            const barWidth = (width - padding * 2) / labels.length;
            const maxValue = Math.max(...data);
            const scale = (height - padding * 2) / maxValue;
            
            labels.forEach((label, index) => {
                const barHeight = data[index] * scale;
                const x = padding + index * barWidth + barWidth * 0.1;
                const y = height - padding - barHeight;
                const width = barWidth * 0.8;
                
                // Draw bar
                ctx.fillStyle = '#3B82F6';
                ctx.fillRect(x, y, width, barHeight);
                
                // Draw label
                ctx.fillStyle = '#000';
                ctx.font = '10px Arial';
                ctx.textAlign = 'center';
                ctx.save();
                ctx.translate(x + width / 2, height - padding + 15);
                ctx.rotate(-Math.PI / 4);
                ctx.fillText(label, 0, 0);
                ctx.restore();
                
                // Draw value
                ctx.fillStyle = '#000';
                ctx.font = '10px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(`₹${this.formatCurrency(data[index])}`, x + width / 2, y - 5);
            });
        }
    }));
});

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('EstimationPro Application Loaded Successfully');
});