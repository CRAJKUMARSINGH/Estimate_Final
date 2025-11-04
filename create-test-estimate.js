import XLSX from 'xlsx';
import fs from 'fs';
import path from 'path';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3001';

// Create a test estimate with real Excel data
async function createTestEstimate() {
    console.log('🏗️ Creating Test Estimate with Real Excel Data...\n');
    
    const estimatePath = 'attached_assets/ESTIMATE_COMMERCIAL_COMPLEX_PANCHAYAT_SAMITI.xlsx';
    
    if (!fs.existsSync(estimatePath)) {
        console.log('❌ Estimate file not found');
        return;
    }
    
    // Read and parse the Excel file
    const buffer = fs.readFileSync(estimatePath);
    const workbook = XLSX.read(buffer, { type: 'buffer' });
    
    console.log(`📊 Parsing Excel file with ${workbook.SheetNames.length} sheets`);
    
    // Extract data from each sheet
    const sheetsData = {};
    const sheetSummary = [];
    
    workbook.SheetNames.forEach(sheetName => {
        console.log(`📋 Processing sheet: "${sheetName}"`);
        
        // Convert sheet to JSON
        const sheetData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { header: 1 });
        
        // Clean and structure the data
        const cleanData = [];
        let headers = [];
        
        // Find the actual headers (skip empty rows)
        for (let i = 0; i < sheetData.length; i++) {
            const row = sheetData[i];
            if (row && row.length > 0 && row.some(cell => cell && String(cell).trim())) {
                // Check if this looks like a header row
                if (row.some(cell => String(cell).toLowerCase().includes('description') || 
                                   String(cell).toLowerCase().includes('s.no') ||
                                   String(cell).toLowerCase().includes('unit') ||
                                   String(cell).toLowerCase().includes('rate'))) {
                    headers = row.map(cell => String(cell || '').trim()).filter(h => h);
                    console.log(`   Found headers: ${headers.join(', ')}`);
                    break;
                }
            }
        }
        
        // If no standard headers found, create generic ones
        if (headers.length === 0) {
            const maxCols = Math.max(...sheetData.map(row => row ? row.length : 0));
            headers = Array.from({length: maxCols}, (_, i) => `Column ${i + 1}`);
        }
        
        // Extract data rows
        let dataStartIndex = 0;
        for (let i = 0; i < sheetData.length; i++) {
            const row = sheetData[i];
            if (row && headers.some(h => row.includes(h))) {
                dataStartIndex = i + 1;
                break;
            }
        }
        
        // Process data rows
        for (let i = dataStartIndex; i < sheetData.length; i++) {
            const row = sheetData[i];
            if (row && row.length > 0 && row.some(cell => cell && String(cell).trim())) {
                const rowData = {};
                headers.forEach((header, index) => {
                    rowData[header] = row[index] || '';
                });
                cleanData.push(rowData);
            }
        }
        
        sheetsData[sheetName] = cleanData;
        sheetSummary.push({
            name: sheetName,
            headers: headers,
            rowCount: cleanData.length
        });
        
        console.log(`   Processed ${cleanData.length} data rows`);
    });
    
    // Send to API via Excel upload endpoint
    try {
        const form = new FormData();
        const excelBuffer = fs.readFileSync(path.resolve(estimatePath));
        const excelBlob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        form.append('file', excelBlob, 'ESTIMATE_COMMERCIAL_COMPLEX_PANCHAYAT_SAMITI.xlsx');
        form.append('projectName', 'COMMERCIAL COMPLEX PANCHAYAT SAMITI');
        form.append('location', 'GIRWA, UDAIPUR');
        form.append('engineerName', 'Test Engineer');
        form.append('referenceNumber', 'EST-001');

        const response = await fetch(`${BASE_URL}/api/excel/upload`, {
            method: 'POST',
            body: form
        });
        
        if (response.ok) {
            const result = await response.json();
            const { estimate, sheetNames, parts } = result;
            console.log(`\n✅ Successfully created estimate: ${estimate.id}`);
            console.log(`📊 Estimate contains ${workbook.SheetNames.length} sheets with real data`);
            console.log(`📑 Server reported sheets: ${sheetNames.length}, parts: ${parts.length}`);

            console.log('\n🧪 Testing SSR insertion endpoint...');
            const ins = await fetch(`${BASE_URL}/api/excel/${estimate.id}/insert-ssr`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ssrItemId: '1', partNumber: 1 })
            });
            console.log(ins.ok ? '✅ Insert SSR API responded OK' : `❌ Insert SSR failed: ${ins.status}`);
            
            console.log(`\n🎯 Test Complete! Visit: ${BASE_URL.replace(/\\/g,'')}/estimate/${estimate.id}`);
            
        } else {
            const error = await response.text();
            console.log(`❌ Failed to create estimate: ${response.status} - ${error}`);
        }
        
    } catch (error) {
        console.log(`❌ Error creating estimate: ${error.message}`);
    }
}

// Run the test
createTestEstimate().catch(console.error);