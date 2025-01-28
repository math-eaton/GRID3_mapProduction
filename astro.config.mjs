// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://math-eaton.github.io',
	base: '/GRID3_mapProduction',
	integrations: [
		starlight({
			title: 'GRID3 Cartographic Standards Manual',
			logo: {
				src: './src/assets/logo.png',
				replacesTitle: false,
			},
			social: {
				github: 'https://github.com/math-eaton/GRID3_mapProduction',
			},
			sidebar: [
				{
					label: 'Manual',
					autogenerate: { directory: 'manual' },
				},
				{
					label: 'Guides',
					autogenerate: { directory: 'guides' },
				},
				{
					label: 'Appendix',
					autogenerate: { directory: 'appendices' },
				},
			],
		}),
	],
});
