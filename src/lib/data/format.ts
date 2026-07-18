import type { FirmName } from './types';

export const FIRMS: FirmName[] = ['Deloitte', 'PwC', 'EY', 'KPMG'];

export const FIRM_COLORS: Record<FirmName, string> = {
	Deloitte: 'var(--firm-deloitte)',
	PwC: 'var(--firm-pwc)',
	EY: 'var(--firm-ey)',
	KPMG: 'var(--firm-kpmg)'
};

export function currencyShort(value: number | null, decimals = 1) {
	if (value == null) return 'Not disclosed';
	if (Math.abs(value) >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(decimals)}B`;
	if (Math.abs(value) >= 1_000_000) return `$${(value / 1_000_000).toFixed(decimals)}M`;
	return new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD',
		maximumFractionDigits: 0
	}).format(value);
}

export function numberShort(value: number | null, decimals = 0) {
	if (value == null) return 'Not disclosed';
	if (Math.abs(value) >= 1_000_000) return `${(value / 1_000_000).toFixed(decimals)}M`;
	if (Math.abs(value) >= 1_000) return `${(value / 1_000).toFixed(decimals)}k`;
	return new Intl.NumberFormat('en-US', { maximumFractionDigits: decimals }).format(value);
}

export function percent(value: number | null, decimals = 1) {
	return value == null ? 'Not disclosed' : `${value.toFixed(decimals)}%`;
}

export function fullNumber(value: number | null) {
	return value == null ? 'Not disclosed' : new Intl.NumberFormat('en-US').format(value);
}

export function formatDate(value: string) {
	if (!value) return 'Not stated';
	return new Intl.DateTimeFormat('en-US', {
		month: 'short',
		day: 'numeric',
		year: 'numeric',
		timeZone: 'UTC'
	}).format(new Date(`${value}T00:00:00Z`));
}

export function displayObservationValue(value: {
	valueOriginal: string;
	valueUsd: number | null;
	valueNumeric: number | null;
	unitOriginal: string;
}) {
	if (value.valueOriginal) return value.valueOriginal;
	if (value.valueUsd != null) return currencyShort(value.valueUsd);
	if (value.valueNumeric != null)
		return `${fullNumber(value.valueNumeric)} ${value.unitOriginal}`.trim();
	return 'Not disclosed';
}
