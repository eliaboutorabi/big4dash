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
		await page.keyboard.press('Escape');
		await expect(page.getByRole('heading', { name: 'Evidence notebook' })).toHaveCount(0);
	});
});
