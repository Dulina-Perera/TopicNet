import { type Writable, writable } from 'svelte/store';

export const boardDraggable: Writable<boolean> = writable(false);
export const boardGrabbing: Writable<boolean> = writable(false);
export const boardScale: Writable<number> = writable(1);
export const boardClickedPos: Writable<{ x: number, y: number }> = writable({ x: -1, y: -1 });
