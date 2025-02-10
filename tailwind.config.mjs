import starlightPlugin from '@astrojs/starlight-tailwind';
import colors from 'tailwindcss/colors';

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
	  extend: {
		colors: {
		  accent: colors.orange,
		  gray: colors.zinc,
		},
		fontFamily: {
		// sans: ['"Helvetica Neue"']
		//   sans: ['"Arial"'],
		//   mono: ['"IBM Plex Mono"'],
		},
	  },
	},
	plugins: [starlightPlugin()],
  };
  