import { join } from 'path';
import { skeleton } from '@skeletonlabs/tw-plugin';

/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
  content: [
		'./src/**/*.{html,js,ts,svelte}',
		join(
			require.resolve('@skeletonlabs/skeleton'),
			'../**/*.{html,js,ts,svelte}'
		)
	],
  theme: {
    extend: {
			colors: {
        'first-color': 'var(--first-color)',
        'title-color': 'var(--title-color)',
        'text-color': 'var(--text-color)',
        'body-color': 'var(--body-color)',
        'container-color': 'var(--container-color)',
        'border-color': 'var(--border-color)',
      },
      fontFamily: {
        body: 'var(--body-font)',
      },
      fontSize: {
        h2: 'var(--h2-font-size)',
        normal: 'var(--normal-font-size)',
      },
      zIndex: {
        fixed: 'var(--z-fixed)',
        modal: 'var(--z-modal)',
      },
      height: {
        header: 'var(--header-height)',
      }
		},
  },
  plugins: [
		skeleton({
			themes: { preset: [ "modern" ] }
		})
	]
}

