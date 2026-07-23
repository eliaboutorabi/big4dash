import { expect, test } from '@playwright/test';

test.describe('FirmScope dashboard', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto('/');
	});

	test('loads the analytical story without interrupting the reader', async ({ page }) => {
		await expect(
			page.getByRole('heading', {
				level: 1,
				name: 'Four networks. One market. Every caveat intact.'
			})
		).toBeVisible();
		await expect(page.getByText('Pairwise workbench')).toBeVisible();
		await expect(page.locator('.driver-popover')).toHaveCount(0);
		await expect(page.getByText('$220B combined')).toBeVisible();
	});

	test('supports comparison, evidence and notebook interactions', async ({ page }) => {
		await page.getByLabel('Choose second network').selectOption('PwC');
		await expect(page.locator('.comparison-row button[data-firm="PwC"]')).toHaveCount(5);

		await page.locator('.comparison-row').first().locator('button').first().click();
		await expect(page.getByRole('dialog', { name: 'Evidence detail' })).toBeVisible();
		await page.getByRole('button', { name: 'Save to notebook' }).click();
		await page.keyboard.press('Escape');
		await expect(page.getByRole('dialog', { name: 'Evidence detail' })).toHaveCount(0);

		await page.getByRole('button', { name: 'Open evidence notebook with 1 saved record' }).click();
		await expect(page.getByRole('heading', { name: 'Evidence notebook' })).toBeVisible();
		await expect(page.getByText('1 saved record')).toBeVisible();
		const downloadPromise = page.waitForEvent('download');
		await page.getByRole('button', { name: 'Download saved evidence as CSV' }).click();
		const download = await downloadPromise;
		expect(download.suggestedFilename()).toMatch(/^firmscope-evidence-\d{4}-\d{2}-\d{2}\.csv$/);
		await page.keyboard.press('Escape');
		await expect(page.getByRole('heading', { name: 'Evidence notebook' })).toHaveCount(0);
	});

	test('updates deeper analytical views from their visible assumptions', async ({ page }) => {
		await page.getByRole('button', { name: 'Show reported revenue share for 2015' }).click();
		await expect(page.locator('.share-chart .chart-caption')).toContainText(
			'2015 · $123.7B combined'
		);

		await page.getByRole('button', { name: '1Y' }).click();
		await expect(page.locator('.scenario-date')).toContainText('FY2026');
		await expect(page.locator('.scenario-readout')).toContainText(
			'above the FY2025 reported baseline after 1 year'
		);

		await page.getByRole('button', { name: /KPMG 8/ }).click();
		await expect(page.locator('.list-heading')).toContainText('8 linked comparisons');
		await expect(page.locator('.inspector-heading')).toContainText('KPMG');
	});

	test('finds and opens evidence from the keyboard command palette', async ({ page }) => {
		await page.locator('body').press('Meta+k');
		await expect(page.getByRole('dialog', { name: 'Go anywhere. Find any fact.' })).toBeVisible();

		const search = page.getByLabel('Search dashboard commands and evidence');
		await search.fill('FY2024 KPMG network revenue');
		await expect(page.locator('.palette-results > button').first()).toContainText(
			'KPMG · Global network revenue'
		);
		await search.press('Enter');

		await expect(page.getByRole('dialog', { name: 'Evidence detail' })).toBeVisible();
		await expect(page.locator('.record-id')).toHaveText('obs_kpmg_0015');
	});
});
