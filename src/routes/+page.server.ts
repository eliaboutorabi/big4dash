import dashboardData from '$lib/data/dashboard-data.json';
import type { DashboardData } from '$lib/data/types';

export function load() {
	return {
		dashboardData: dashboardData as DashboardData
	};
}
