import { inflateRawSync } from 'node:zlib';

const directoryIndexUrl = 'https://kpmg.com/xx/en/misc/request-for-proposal.html';
const geonamesUrl = 'https://download.geonames.org/export/dump/cities500.zip';
const countryInfoUrl = 'https://download.geonames.org/export/dump/countryInfo.txt';
const retrievedAt = '2026-07-18';

function plainText(value = '') {
	return String(value)
		.replace(/<script[\s\S]*?<\/script>/gi, ' ')
		.replace(/<style[\s\S]*?<\/style>/gi, ' ')
		.replace(/<[^>]+>/g, ' ')
		.replace(/&amp;/g, '&')
		.replace(/&nbsp;/g, ' ')
		.replace(/&#39;/g, "'")
		.replace(/&quot;/g, '"')
		.replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
		.replace(/\s+/g, ' ')
		.trim();
}

function normalized(value = '') {
	return plainText(value)
		.toLowerCase()
		.normalize('NFKD')
		.replace(/[\u0300-\u036f]/g, '')
		.replace(/&/g, 'and')
		.replace(/[^a-z0-9]+/g, ' ')
		.trim();
}

function unzipFirstEntry(archive) {
	let endOffset = archive.length - 22;
	while (endOffset >= 0 && archive.readUInt32LE(endOffset) !== 0x06054b50) endOffset -= 1;
	if (endOffset < 0) throw new Error('GeoNames ZIP end record was not found');
	const directoryOffset = archive.readUInt32LE(endOffset + 16);
	if (archive.readUInt32LE(directoryOffset) !== 0x02014b50) {
		throw new Error('GeoNames ZIP central directory was not found');
	}
	const compression = archive.readUInt16LE(directoryOffset + 10);
	const compressedSize = archive.readUInt32LE(directoryOffset + 20);
	const localOffset = archive.readUInt32LE(directoryOffset + 42);
	const nameLength = archive.readUInt16LE(localOffset + 26);
	const extraLength = archive.readUInt16LE(localOffset + 28);
	const dataOffset = localOffset + 30 + nameLength + extraLength;
	const payload = archive.subarray(dataOffset, dataOffset + compressedSize);
	if (compression === 0) return payload.toString('utf8');
	if (compression === 8) return inflateRawSync(payload).toString('utf8');
	throw new Error(`Unsupported GeoNames ZIP compression method ${compression}`);
}

async function fetchText(url, timeout = 15_000) {
	const response = await fetch(url, {
		headers: { 'user-agent': 'FirmScope office research/1.0' },
		signal: AbortSignal.timeout(timeout),
		redirect: 'follow'
	});
	if (!response.ok) throw new Error(`${response.status} ${url}`);
	return { text: await response.text(), url: response.url };
}

async function mapLimit(items, limit, mapper) {
	const results = new Array(items.length);
	let next = 0;
	async function worker() {
		while (next < items.length) {
			const index = next++;
			try {
				results[index] = await mapper(items[index], index);
			} catch {
				results[index] = null;
			}
		}
	}
	await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
	return results;
}

const [directoryIndex, countryInfoResponse, citiesResponse] = await Promise.all([
	fetchText(directoryIndexUrl, 30_000),
	fetch(countryInfoUrl),
	fetch(geonamesUrl)
]);

const countryInfoText = await countryInfoResponse.text();
const countryByCode = new Map();
for (const line of countryInfoText.split('\n')) {
	if (!line || line.startsWith('#')) continue;
	const fields = line.split('\t');
	countryByCode.set(fields[0], { code: fields[0], name: fields[4] });
}

const citiesArchive = Buffer.from(await citiesResponse.arrayBuffer());
const citiesText = unzipFirstEntry(citiesArchive);
const cityIndexes = new Map();
for (const line of citiesText.split('\n')) {
	if (!line) continue;
	const fields = line.split('\t');
	const countryCode = fields[8];
	const city = {
		name: fields[1],
		latitude: Number(fields[4]),
		longitude: Number(fields[5]),
		population: Number(fields[14]) || 0
	};
	if (!Number.isFinite(city.latitude) || !Number.isFinite(city.longitude)) continue;
	if (!cityIndexes.has(countryCode)) cityIndexes.set(countryCode, new Map());
	const index = cityIndexes.get(countryCode);
	const aliases = new Set([fields[1], fields[2], ...(fields[3] || '').split(',')]);
	for (const alias of aliases) {
		const key = normalized(alias);
		if (!key) continue;
		const current = index.get(key);
		if (!current || city.population > current.population) index.set(key, city);
	}
}

const localesByRoute = new Map();
for (const match of directoryIndex.text.matchAll(/value="(https:\/\/kpmg\.com\/[^"\s]+)[^"]*"/gi)) {
	try {
		const url = new URL(match[1]);
		const [routeCode, locale] = url.pathname.split('/').filter(Boolean);
		if (!routeCode || routeCode === 'xx' || !locale) continue;
		if (!localesByRoute.has(routeCode)) localesByRoute.set(routeCode, new Set());
		localesByRoute.get(routeCode).add(locale);
	} catch {
		// Ignore malformed legacy form targets.
	}
}

for (const [routeCode, locale] of Object.entries({
	de: 'en',
	dk: 'en',
	es: 'en',
	fr: 'en',
	it: 'en',
	jp: 'en',
	mx: 'en',
	nl: 'en',
	pt: 'en',
	sg: 'en'
})) {
	if (!localesByRoute.has(routeCode)) localesByRoute.set(routeCode, new Set());
	localesByRoute.get(routeCode).add(locale);
}

const routeCodeToCountryCode = (routeCode) => (routeCode === 'uk' ? 'GB' : routeCode.toUpperCase());
const routes = [...localesByRoute]
	.map(([routeCode, locales]) => ({
		routeCode,
		countryCode: routeCodeToCountryCode(routeCode),
		locales: [...locales]
	}))
	.filter((entry) => countryByCode.has(entry.countryCode) && cityIndexes.has(entry.countryCode));

function candidateNames(label) {
	const raw = plainText(label);
	const withoutKpmg = raw
		.replace(/^kpmg\s+(in\s+)?/i, '')
		.replace(/,?\s+kpmg\b.*$/i, '')
		.trim();
	return [
		raw,
		withoutKpmg,
		withoutKpmg.split('|')[0],
		withoutKpmg.split(',')[0],
		withoutKpmg.split(/\s+-\s+/)[0],
		withoutKpmg.replace(/\s*\([^)]*\)\s*/g, ' ')
	]
		.map(normalized)
		.filter(Boolean);
}

function cityForLabel(countryCode, label) {
	const index = cityIndexes.get(countryCode);
	if (!index) return null;
	for (const candidate of candidateNames(label)) {
		const direct = index.get(candidate);
		if (direct) return direct;
	}
	return null;
}

async function findDirectoryPage(route) {
	const paths = [];
	for (const locale of new Set(['en', ...route.locales])) {
		paths.push(
			`${locale}/about/offices.html`,
			`${locale}/about-us/offices.html`,
			`${locale}/about/office-locations.html`,
			`${locale}/about-us/office-locations.html`,
			`${locale}/how-we-work/locations.html`,
			`${locale}/home/about/offices.html`
		);
	}
	for (const path of paths) {
		const requestedUrl = `https://kpmg.com/${route.routeCode}/${path}`;
		try {
			const page = await fetchText(requestedUrl);
			const title = plainText(page.text.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]);
			if (
				!/office|location|standort|bureau|sede|oficina|vestiging|kontor|biur|kantoor/i.test(title)
			) {
				continue;
			}
			return { ...page, title };
		} catch {
			// Try the next official route pattern.
		}
	}
	return null;
}

const pages = await mapLimit(routes, 14, async (route) => ({
	route,
	page: await findDirectoryPage(route)
}));

const records = [];
const sourcePages = [];
for (const result of pages.filter(Boolean)) {
	const { route, page } = result;
	if (!page) continue;
	sourcePages.push(page.url);
	const labels = [...page.text.matchAll(/<h[2-5][^>]*>([\s\S]*?)<\/h[2-5]>/gi)].map((match) =>
		plainText(match[1])
	);
	if (route.countryCode === 'US') {
		for (const match of page.text.matchAll(/href="[^"]*\/locations\/([^/"?#]+)\.html/gi)) {
			labels.push(match[1].replaceAll('-', ' '));
		}
	}
	for (const label of new Set(labels)) {
		const city = cityForLabel(route.countryCode, label);
		if (!city) continue;
		records.push({
			city: city.name,
			country: countryByCode.get(route.countryCode).name,
			countryCode: route.countryCode,
			latitude: city.latitude,
			longitude: city.longitude,
			sourceUrl: page.url
		});
	}
}

const uniqueRecords = [
	...new Map(
		records.map((record) => [
			`${record.countryCode}|${record.latitude}|${record.longitude}`,
			record
		])
	).values()
].sort((a, b) => a.country.localeCompare(b.country) || a.city.localeCompare(b.city));

process.stdout.write(
	`${JSON.stringify(
		{
			sourceIndexUrl: directoryIndexUrl,
			retrievedAt,
			coordinateMethod:
				'Official KPMG country-directory city labels joined to GeoNames city centroids',
			sourcePageCount: new Set(sourcePages).size,
			mappedRecordCount: uniqueRecords.length,
			records: uniqueRecords
		},
		null,
		2
	)}\n`
);
