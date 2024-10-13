import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';

export const customTheme: CustomThemeConfig = {
    name: 'custom-theme',
    properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-family-heading": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-color-base": "#000",
		"--theme-font-color-dark": "#fff",
		"--theme-rounded-base": "12px",
		"--theme-rounded-container": "8px",
		"--theme-border-base": "1px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "255 255 255",
		"--on-secondary": "0 0 0",
		"--on-tertiary": "0 0 0",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "255 255 255",
		"--on-surface": "255 255 255",
		// =~= Theme Colors  =~=
		// primary | #0d1a66
		"--color-primary-50": "#dbdde8",
		"--color-primary-100": "#cfd1e0",
		"--color-primary-200": "#c3c6d9",
		"--color-primary-300": "#9ea3c2",
		"--color-primary-400": "86 95 148", // #565f94
		"--color-primary-500": "13 26 102", // #0d1a66
		"--color-primary-600": "12 23 92", // #0c175c
		"--color-primary-700": "#0a144d",
		"--color-primary-800": "8 16 61", // #08103d
		"--color-primary-900": "6 13 50", // #060d32
		// secondary | #948bb7
		"--color-secondary-50": "239 238 244", // #efeef4
		"--color-secondary-100": "#eae8f1",
		"--color-secondary-200": "#e4e2ed",
		"--color-secondary-300": "#d4d1e2",
		"--color-secondary-400": "#b4aecd",
		"--color-secondary-500": "148 139 183", // #948bb7
		"--color-secondary-600": "133 125 165", // #857da5
		"--color-secondary-700": "111 104 137", // #6f6889
		"--color-secondary-800": "#59536e",
		"--color-secondary-900": "73 68 90", // #49445a
		// tertiary | #d2c1ff
		"--color-tertiary-50": "248 246 255", // #f8f6ff
		"--color-tertiary-100": "246 243 255", // #f6f3ff
		"--color-tertiary-200": "#f4f0ff",
		"--color-tertiary-300": "#ede6ff",
		"--color-tertiary-400": "224 212 255", // #e0d4ff
		"--color-tertiary-500": "210 193 255", // #d2c1ff
		"--color-tertiary-600": "189 174 230", // #bdaee6
		"--color-tertiary-700": "158 145 191", // #9e91bf
		"--color-tertiary-800": "126 116 153", // #7e7499
		"--color-tertiary-900": "103 95 125", // #675f7d
		// success | #00c89b
		"--color-success-50": "217 247 240", // #d9f7f0
		"--color-success-100": "204 244 235", // #ccf4eb
		"--color-success-200": "191 241 230", // #bff1e6
		"--color-success-300": "153 233 215", // #99e9d7
		"--color-success-400": "77 217 185", // #4dd9b9
		"--color-success-500": "0 200 155", // #00c89b
		"--color-success-600": "0 180 140", // #00b48c
		"--color-success-700": "0 150 116", // #009674
		"--color-success-800": "0 120 93", // #00785d
		"--color-success-900": "0 98 76", // #00624c
		// warning | #ffb451
		"--color-warning-50": "255 244 229", // #fff4e5
		"--color-warning-100": "255 240 220", // #fff0dc
		"--color-warning-200": "255 236 212", // #ffecd4
		"--color-warning-300": "255 225 185", // #ffe1b9
		"--color-warning-400": "255 203 133", // #ffcb85
		"--color-warning-500": "255 180 81", // #ffb451
		"--color-warning-600": "230 162 73", // #e6a249
		"--color-warning-700": "191 135 61", // #bf873d
		"--color-warning-800": "153 108 49", // #996c31
		"--color-warning-900": "125 88 40", // #7d5828
		// error | #9a0a1e
		"--color-error-50": "240 218 221", // #f0dadd
		"--color-error-100": "235 206 210", // #ebced2
		"--color-error-200": "230 194 199", // #e6c2c7
		"--color-error-300": "215 157 165", // #d79da5
		"--color-error-400": "184 84 98", // #b85462
		"--color-error-500": "154 10 30", // #9a0a1e
		"--color-error-600": "139 9 27", // #8b091b
		"--color-error-700": "116 8 23", // #740817
		"--color-error-800": "92 6 18", // #5c0612
		"--color-error-900": "75 5 15", // #4b050f
		// surface | #3b57e3
		"--color-surface-50": "#e2e6fb",
		"--color-surface-100": "#d8ddf9",
		"--color-surface-200": "#ced5f8",
		"--color-surface-300": "#b1bcf4",
		"--color-surface-400": "#7689eb",
		"--color-surface-500": "#3b57e3",
		"--color-surface-600": "#354ecc",
		"--color-surface-700": "#2c41aa",
		"--color-surface-800": "#233488",
		"--color-surface-900": "#1d2b6f",
	}
}
