// Create a simple test estimate
async function createSimpleEstimate() {
    console.log('🏗️ Creating Simple Test Estimate...\n');
    
    const BASE_URL = process.env.BASE_URL || 'http://localhost:3001';
    const filePath = 'attached_assets/ESTIMATE_COMMERCIAL_COMPLEX_PANCHAYAT_SAMITI.xlsx';

    try {
        const form = new FormData();
        const excelBuffer = fs.readFileSync(filePath);
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
            const { estimate, sheetNames, parts } = await response.json();
            console.log(`✅ Successfully created estimate: ${estimate.id}`);
            console.log(`📊 File uploaded and parsed server-side. Sheets: ${sheetNames.length}, parts: ${parts.length}`);
            
            console.log('\n🧪 Testing sheet data retrieval...');
            console.log('\n🧪 Testing SSR insertion endpoint...');
            const ins = await fetch(`${BASE_URL}/api/excel/${estimate.id}/insert-ssr`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ssrItemId: '1', partNumber: 1 })
            });
            console.log(ins.ok ? '✅ Insert SSR API responded OK' : `❌ Insert SSR failed: ${ins.status}`);
            
            console.log(`\n🎯 Test Complete!`);
            console.log(`🌐 Visit: ${BASE_URL}/estimate/${estimate.id}`);
            console.log(`📋 Or check estimates: ${BASE_URL}/estimates`);
            
            return estimate.id;
            
        } else {
            const error = await response.text();
            console.log(`❌ Failed to create estimate: ${response.status} - ${error}`);
        }
        
    } catch (error) {
        console.log(`❌ Error creating estimate: ${error.message}`);
    }
}

// Run the test
createSimpleEstimate().catch(console.error);