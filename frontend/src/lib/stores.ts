// frontend/src/lib/stores.ts

import type { User } from '@prisma/client';
import { writable } from 'svelte/store';

// Initially, the user is set to null (not logged in).
export const user = writable<User | null>(null);

// When the user logs in, update the user store.
export const setUser = (authenticatedUser: User) => {
	user.set(authenticatedUser);
};

// When the user logs out, update the user store.
export const clearUser = () => {
	user.set(null);
};

// Initially, the search component is not visible.
export const searchVisible = writable(false);

// Initially, the login component is not visible.
export const loginVisible = writable(false);

// Initially, the board is not grabbed.
export const grabbingBoard = writable(false);

// Initially, the board is not scaled.
export const boardScale = writable(1);

// Initially, the board is not clicked.
export const boardClickedPosition = writable({ x: -1, y: -1 });
