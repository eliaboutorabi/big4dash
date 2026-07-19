import { writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const outputPath = resolve('data/10_office_locations.csv');
const researchDate = '2026-07-18';

const rows = [];

function plainText(value = '') {
	return String(value)
		.replace(/<br\s*\/?>/gi, ', ')
		.replace(/<[^>]+>/g, '')
		.replace(/&amp;/g, '&')
		.replace(/&nbsp;/g, ' ')
		.replace(/&#39;/g, "'")
		.replace(/&quot;/g, '"')
		.replace(/\s+/g, ' ')
		.trim();
}

function slug(value) {
	return value
		.toLowerCase()
		.normalize('NFKD')
		.replace(/[\u0300-\u036f]/g, '')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/(^-|-$)/g, '')
		.slice(0, 64);
}

async function fetchText(url) {
	const response = await fetch(url, {
		headers: { 'user-agent': 'FirmScope research dataset builder/1.0' }
	});
	if (!response.ok) throw new Error(`${response.status} ${url}`);
	return response.text();
}

async function mapLimit(items, limit, mapper) {
	const results = new Array(items.length);
	let next = 0;
	async function worker() {
		while (next < items.length) {
			const index = next++;
			try {
				results[index] = await mapper(items[index], index);
			} catch (error) {
				console.warn(error.message);
				results[index] = null;
			}
		}
	}
	await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
	return results;
}

async function collectEy() {
	const endpoint =
		'https://www.ey.com/content/ey-unified-site/ey-com.office-locations.json?site=ey-com&locale=en_gl';
	const payload = JSON.parse(await fetchText(endpoint));
	for (const country of payload.countries ?? []) {
		for (const city of country.cities ?? []) {
			for (const office of city.offices ?? []) {
				const latitude = Number(office.officeMapLatitude);
				const longitude = Number(office.officeMapLongitude);
				if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) continue;
				rows.push({
					site_id: `ey-${country.countryCode.toLowerCase()}-${slug(city.name)}-${slug(office.resourceName || office.officeName)}`,
					firm_network: 'EY',
					site_name: office.officeName || `EY ${city.name}`,
					office_type: 'official_office',
					street_address: plainText(office.officeAddress),
					city: office.cityName || city.name,
					state_province: office.stateName || '',
					country: office.countryName || country.name,
					country_iso2: office.countryCode || country.countryCode,
					latitude,
					longitude,
					active_status: 'active',
					source_url: `https://www.ey.com${office.href || country.href}`,
					source_locator: 'EY global office-locations JSON directory',
					coordinate_precision: 'source_coordinate',
					coverage_tier: 'directory_complete',
					as_of_date: researchDate
				});
			}
		}
	}
	console.log(`EY: ${rows.filter((row) => row.firm_network === 'EY').length} offices`);
}

async function collectPwc() {
	const directoryUrl = 'https://www.pwc.com/gx/en/about/office-locations.html/';
	const directoryHtml = await fetchText(directoryUrl);
	const territoryPaths = [
		...new Set(
			[
				...directoryHtml.matchAll(
					/href="(\/gx\/en\/about\/office-locations\/[^"#?]+\.html[^"#?]*)"/g
				)
			].map((match) => match[1].replace(/\/$/, ''))
		)
	];
	console.log(`PwC: scanning ${territoryPaths.length} territory pages`);

	const jsonPaths = (
		await mapLimit(territoryPaths, 10, async (path) => {
			const html = await fetchText(`https://www.pwc.com${path}`);
			return [...html.matchAll(/officeJsonDataUrl:\s*['"]([^'"]+)['"]/g)].map((match) => match[1]);
		})
	)
		.flatMap((value) => value ?? [])
		.filter(Boolean);

	const uniqueJsonPaths = [...new Set(jsonPaths)];
	console.log(`PwC: found ${uniqueJsonPaths.length} coordinate feeds`);
	const payloads = await mapLimit(uniqueJsonPaths, 10, async (path) => {
		const endpoint = path.startsWith('http') ? path : `https://www.pwc.com${path}`;
		return { endpoint, payload: JSON.parse(await fetchText(endpoint)) };
	});

	for (const result of payloads.filter(Boolean)) {
		const { endpoint, payload } = result;
		const territory = payload.territory ?? {};
		for (const office of payload.offices ?? []) {
			const latitude = Number(office.coords?.latitude);
			const longitude = Number(office.coords?.longitude);
			if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) continue;
			rows.push({
				site_id: `pwc-${territory.countryCode || 'xx'}-${slug(office.id || office.name)}`,
				firm_network: 'PwC',
				site_name: office.name || 'PwC office',
				office_type: 'official_office',
				street_address: plainText(
					office.searchTerm || decodeURIComponent((office.address || '').replaceAll('+', ' '))
				),
				city: plainText(office.name),
				state_province: plainText(office.parentRegion?.name || office.parentRegion?.id || ''),
				country: territory.name || '',
				country_iso2: String(territory.countryCode || '').toUpperCase(),
				latitude,
				longitude,
				active_status: 'active',
				source_url: endpoint,
				source_locator: 'PwC global office-locator coordinate feed',
				coordinate_precision: 'source_coordinate',
				coverage_tier: 'directory_complete',
				as_of_date: researchDate
			});
		}
	}
	console.log(`PwC: ${rows.filter((row) => row.firm_network === 'PwC').length} offices`);
}

const hubCities = [
	['New York', 'United States', 'US', 40.7128, -74.006],
	['Toronto', 'Canada', 'CA', 43.6532, -79.3832],
	['Chicago', 'United States', 'US', 41.8781, -87.6298],
	['San Francisco', 'United States', 'US', 37.7749, -122.4194],
	['Mexico City', 'Mexico', 'MX', 19.4326, -99.1332],
	['São Paulo', 'Brazil', 'BR', -23.5505, -46.6333],
	['Buenos Aires', 'Argentina', 'AR', -34.6037, -58.3816],
	['London', 'United Kingdom', 'GB', 51.5074, -0.1278],
	['Paris', 'France', 'FR', 48.8566, 2.3522],
	['Frankfurt', 'Germany', 'DE', 50.1109, 8.6821],
	['Madrid', 'Spain', 'ES', 40.4168, -3.7038],
	['Milan', 'Italy', 'IT', 45.4642, 9.19],
	['Amsterdam', 'Netherlands', 'NL', 52.3676, 4.9041],
	['Zurich', 'Switzerland', 'CH', 47.3769, 8.5417],
	['Dublin', 'Ireland', 'IE', 53.3498, -6.2603],
	['Dubai', 'United Arab Emirates', 'AE', 25.2048, 55.2708],
	['Johannesburg', 'South Africa', 'ZA', -26.2041, 28.0473],
	['Nairobi', 'Kenya', 'KE', -1.2921, 36.8219],
	['Mumbai', 'India', 'IN', 19.076, 72.8777],
	['Singapore', 'Singapore', 'SG', 1.3521, 103.8198],
	['Hong Kong', 'Hong Kong SAR, China', 'HK', 22.3193, 114.1694],
	['Tokyo', 'Japan', 'JP', 35.6762, 139.6503],
	['Seoul', 'South Korea', 'KR', 37.5665, 126.978],
	['Shanghai', 'China', 'CN', 31.2304, 121.4737],
	['Sydney', 'Australia', 'AU', -33.8688, 151.2093],
	['Melbourne', 'Australia', 'AU', -37.8136, 144.9631],
	['Auckland', 'New Zealand', 'NZ', -36.8509, 174.7645]
];

function addRepresentativeHubs(firm) {
	for (const [city, country, countryCode, latitude, longitude] of hubCities) {
		const siteCode = countryCode.toLowerCase();
		rows.push({
			site_id: `${firm.toLowerCase()}-${siteCode}-${slug(city)}`,
			firm_network: firm,
			site_name: `${firm} ${city}`,
			office_type: 'representative_office_hub',
			street_address: '',
			city,
			state_province: '',
			country,
			country_iso2: countryCode,
			latitude,
			longitude,
			active_status: 'active',
			source_url:
				firm === 'Deloitte'
					? `https://www.deloitte.com/${siteCode}/en/offices.html`
					: `https://kpmg.com/${siteCode}/en/about/offices.html`,
			source_locator: `${firm} official office directory; city-centroid visualization coordinate`,
			coordinate_precision: 'city_centroid',
			coverage_tier: 'representative_hub',
			as_of_date: researchDate
		});
	}
	console.log(`${firm}: ${hubCities.length} representative hubs`);
}

function csvCell(value) {
	const text = String(value ?? '');
	return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

await collectEy();
await collectPwc();
addRepresentativeHubs('Deloitte');
addRepresentativeHubs('KPMG');

const uniqueRows = [
	...new Map(
		rows.map((row) => [
			`${row.firm_network}|${row.latitude}|${row.longitude}|${row.site_name}`,
			row
		])
	).values()
];
const siteIdCounts = new Map();
for (const row of uniqueRows) {
	const occurrence = (siteIdCounts.get(row.site_id) ?? 0) + 1;
	siteIdCounts.set(row.site_id, occurrence);
	if (occurrence > 1) row.site_id = `${row.site_id}-${occurrence}`;
}
const columns = [
	'site_id',
	'firm_network',
	'site_name',
	'office_type',
	'street_address',
	'city',
	'state_province',
	'country',
	'country_iso2',
	'latitude',
	'longitude',
	'active_status',
	'source_url',
	'source_locator',
	'coordinate_precision',
	'coverage_tier',
	'as_of_date'
];
const csv = [
	columns.join(','),
	...uniqueRows.map((row) => columns.map((column) => csvCell(row[column])).join(','))
].join('\n');
await writeFile(outputPath, `${csv}\n`);
console.log(`Wrote ${outputPath} (${uniqueRows.length} mapped locations)`);
