// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from '@astrojs/tailwind';

import icon from 'astro-icon';

// https://astro.build/config
export default defineConfig({
    site: 'https://math-eaton.github.io',
    base: '/GRID3_mapProduction',
    integrations: [starlight({
        title: 'GRID3 Cartographic Standards Manual',
        logo: {
            src: './src/assets/logo.png',
            replacesTitle: false,
        },
        favicon: './favicon.png',
        customCss: [
            './src/styles/tailwind.css',
            // '@fontsource/fontsource/lato',
          ],	
        social: {
            github: 'https://github.com/math-eaton/GRID3_mapProduction',
        },
        sidebar: [
            {
                label: 'Manual',
                autogenerate: { directory: '01-manual' },
            },
            {
                label: 'Style guide',
                autogenerate: { directory: '02-style' },
            },
            {
                label: 'Tutorials',
                autogenerate: { directory: '03-tutorials' },
            },
            {
                label: 'Appendix',
                autogenerate: { directory: '04-appendices' },
                collapsed: true,
            },
            { 
                label: 'GRID3 data',
                link: 'https://data.grid3.org/',
                // badge: { text: 'External', variant: 'caution' },
            },
            { 
                label: 'GitHub',
                link: 'https://github.com/math-eaton/GRID3_mapProduction/tree/main/scripts/', 
                // badge: { text: 'External', variant: 'caution' },
            },



        ],
    }), tailwind({
        // Disable the default base styles:
        applyBaseStyles: false,
        }), icon()],
});