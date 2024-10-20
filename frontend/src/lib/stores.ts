import { writable, type Writable } from 'svelte/store';

export const theme: Writable<string> = writable("dark"); // Default theme is dark.

export const navMenuVisible: Writable<boolean> = writable(false);
export const loginVisible: Writable<boolean> = writable(true);

export const boardDraggable: Writable<boolean> = writable(false);
export const boardGrabbing: Writable<boolean> = writable(false);
export const boardScale: Writable<number> = writable(1);
export const boardClickedPos: Writable<{ x: number, y: number }> = writable({ x: -1, y: -1 });
