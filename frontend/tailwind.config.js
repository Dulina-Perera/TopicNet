/** @type {import("tailwindcss").Config} */
export default {
	content: ["./src/**/*.{html,js,ts,svelte}"],
	theme: {
		container: {
			center: true,
			padding: "2rem",
			screens: {
				"2xl": "1440px",
			}
		},
		extend: {
			colors: {
        colors: {
					primary: "var(--theme-primary-color)",
					title: "var(--theme-title-color)",
					text: "var(--theme-text-color)",
					body: "var(--theme-body-color)",
					container: "var(--theme-container-color)",
					border: "var(--theme-border-color)",
				},
				fontFamily: {
					logo: "var(--theme-font-family-logo)",
					base: "var(--theme-font-family-base)",
				},
				fontSize: {
					h2: "var(--theme-font-size-h2)",
					normal: "var(--theme-font-size-normal)",
				},
				borderRadius: {
					base: "var(--theme-border-radius-base)",
					container: "var(--theme-border-radius-container)",
				},
				zIndex: {
					tooltip: "var(--theme-z-index-tooltip)",
					fixed: "var(--theme-z-index-fixed)",
					modal: "var(--theme-z-index-modal)",
				}
			}
		}
	},
	plugins: []
}
