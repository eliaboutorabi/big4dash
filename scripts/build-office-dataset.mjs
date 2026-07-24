import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const outputPath = resolve('data/10_office_locations.csv');
const deloitteDirectoryPath = resolve('data/sources/deloitte-office-directory.json');
const kpmgDirectoryPath = resolve('data/sources/kpmg-office-directory.json');
const researchDate = '2026-07-18';
const regionNames = new Intl.DisplayNames(['en'], { type: 'region' });

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

function validCountryCode(value) {
	const code = String(value ?? '')
		.trim()
		.toUpperCase();
	return /^[A-Z]{2}$/.test(code) ? code : '';
}

function pwcCountry(territory, office) {
	const territoryName = plainText(territory.name);
	const territoryCode = validCountryCode(territory.countryCode);
	const officeCode = validCountryCode(String(office.id ?? '').split('-')[0]);
	const countryCode = territoryCode || officeCode;
	const isPlaceholder = /choose a territory/i.test(territoryName);
	let country = isPlaceholder ? '' : territoryName;

	if (!country && countryCode) {
		try {
			country = regionNames.of(countryCode) ?? '';
		} catch {
			country = '';
		}
	}

	if (!country) country = plainText(office.parentRegion?.name || office.parentRegion?.id || '');
	return { country, countryCode, isPlaceholder };
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
			const resolvedCountry = pwcCountry(territory, office);
			rows.push({
				site_id: `pwc-${resolvedCountry.countryCode.toLowerCase() || 'xx'}-${slug(office.id || office.name)}`,
				firm_network: 'PwC',
				site_name: office.name || 'PwC office',
				office_type: 'official_office',
				street_address: plainText(
					office.searchTerm || decodeURIComponent((office.address || '').replaceAll('+', ' '))
				),
				city: plainText(office.name),
				state_province: resolvedCountry.isPlaceholder
					? ''
					: plainText(office.parentRegion?.name || office.parentRegion?.id || ''),
				country: resolvedCountry.country,
				country_iso2: resolvedCountry.countryCode,
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

async function collectDeloitte() {
	const snapshot = JSON.parse(await readFile(deloitteDirectoryPath, 'utf8'));
	for (const [index, office] of snapshot.records.entries()) {
		const latitude = Number(office.lat);
		const longitude = Number(office.lon);
		if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) continue;
		rows.push({
			site_id: `deloitte-${slug(office.country)}-${slug(office.city)}-${index + 1}`,
			firm_network: 'Deloitte',
			site_name: `Deloitte ${office.city}`,
			office_type: 'official_directory_location',
			street_address: plainText(office.address),
			city: plainText(office.city),
			state_province: '',
			country: plainText(office.country),
			country_iso2: '',
			latitude,
			longitude,
			active_status: 'active',
			source_url: office.detailUrl || snapshot.sourceUrl,
			source_locator: `Deloitte global office directory; source-linked map coordinate (${snapshot.mappedRecordCount} mapped of ${snapshot.directoryRecordCount} directory entries)`,
			coordinate_precision: 'source_coordinate',
			coverage_tier: 'directory_mapped',
			as_of_date: snapshot.retrievedAt || researchDate
		});
	}
	console.log(
		`Deloitte: ${snapshot.mappedRecordCount} mapped of ${snapshot.directoryRecordCount} directory entries`
	);
}

async function collectKpmg() {
	const snapshot = JSON.parse(await readFile(kpmgDirectoryPath, 'utf8'));
	for (const [index, office] of snapshot.records.entries()) {
		const latitude = Number(office.latitude);
		const longitude = Number(office.longitude);
		if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) continue;
		rows.push({
			site_id: `kpmg-${office.countryCode.toLowerCase()}-${slug(office.city)}-${index + 1}`,
			firm_network: 'KPMG',
			site_name: `KPMG ${office.city}`,
			office_type: 'official_directory_location',
			street_address: '',
			city: plainText(office.city),
			state_province: '',
			country: plainText(office.country),
			country_iso2: office.countryCode,
			latitude,
			longitude,
			active_status: 'active',
			source_url: office.sourceUrl || snapshot.sourceIndexUrl,
			source_locator: 'KPMG official country office directory; GeoNames city-centroid coordinate',
			coordinate_precision: 'city_centroid',
			coverage_tier: 'directory_mapped',
			as_of_date: snapshot.retrievedAt || researchDate
		});
	}
	console.log(
		`KPMG: ${snapshot.mappedRecordCount} locations normalized from ${snapshot.sourcePageCount} official directory pages`
	);
}

function csvCell(value) {
	const text = String(value ?? '');
	return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

await collectEy();
await collectPwc();
await collectDeloitte();
await collectKpmg();

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
const invalidCountryRows = uniqueRows.filter(
	(row) => !row.country || /choose a territory/i.test(row.country)
);
if (invalidCountryRows.length > 0) {
	throw new Error(
		`Office dataset contains ${invalidCountryRows.length} missing or placeholder countries; first invalid site: ${invalidCountryRows[0].site_id}`
	);
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
