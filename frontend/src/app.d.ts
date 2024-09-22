// frontend/src/app.d.ts

import type { PrismaClient } from "@prisma/client";

// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	};

	// eslint-disable-next-line no-var
	var prismaClient: PrismaClient;
}

export {};
