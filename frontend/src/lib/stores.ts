import { writable } from 'svelte/store';

// To manage the theme, we need to store the current theme.
export const theme = writable("dark"); // Default theme is dark.
