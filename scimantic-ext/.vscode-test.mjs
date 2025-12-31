import { defineConfig } from '@vscode/test-cli';

export default defineConfig({
	files: 'out/test/**/*.test.js',
	// Run in headless mode for CI and pre-commit hooks
	launchArgs: [
		'--disable-extensions',
		'--disable-gpu',
		'--no-sandbox',
	],
	// Set timeout to prevent hanging
	mocha: {
		timeout: 20000,
	},
});
