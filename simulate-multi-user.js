import fs from 'fs';
import path from 'path';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3001';

async function uploadEstimate(userIndex) {
	const estimatePath = 'attached_assets/ESTIMATE_COMMERCIAL_COMPLEX_PANCHAYAT_SAMITI.xlsx';
	const buffer = fs.readFileSync(path.resolve(estimatePath));
	const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

	const form = new FormData();
	form.append('file', blob, `COMMERCIAL_COMPLEX_${userIndex}.xlsx`);
	form.append('projectName', `COMMERCIAL COMPLEX - USER ${userIndex}`);
	form.append('location', 'GIRWA, UDAIPUR');
	form.append('engineerName', `Engineer ${userIndex}`);
	form.append('referenceNumber', `EST-${String(userIndex).padStart(3,'0')}`);

	const res = await fetch(`${BASE_URL}/api/excel/upload`, { method: 'POST', body: form });
	if (!res.ok) throw new Error(`Upload failed (${userIndex}): ${res.status}`);
	return res.json();
}

async function insertSSR(estimateId) {
	const res = await fetch(`${BASE_URL}/api/excel/${estimateId}/insert-ssr`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ ssrItemId: '1', partNumber: 1 })
	});
	return res.ok;
}

async function verifyEstimate(estimateId) {
	const res = await fetch(`${BASE_URL}/api/estimates/${estimateId}`);
	if (!res.ok) return false;
	const est = await res.json();
	return Boolean(est && est.id === estimateId);
}

async function main() {
	console.log(`👥 Simulating 15 users against ${BASE_URL}...`);
	const results = [];
	for (let i = 1; i <= 15; i++) {
		try {
			const { estimate } = await uploadEstimate(i);
			const ssrOK = await insertSSR(estimate.id);
			const verifyOK = await verifyEstimate(estimate.id);
			results.push({ i, estimateId: estimate.id, ssrOK, verifyOK });
			console.log(`✅ User ${i}: est=${estimate.id}, SSR=${ssrOK ? 'OK' : 'FAIL'}, Verify=${verifyOK ? 'OK' : 'FAIL'}`);
		} catch (err) {
			results.push({ i, error: err.message });
			console.log(`❌ User ${i} failed: ${err.message}`);
		}
	}

	const ok = results.filter(r => !r.error).length;
	console.log(`\n📊 Simulation complete: ${ok}/15 successful.`);
}

main().catch(err => {
	console.error('Simulation error:', err);
	process.exit(1);
});
