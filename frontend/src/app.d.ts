import type { PrismaClient } from "@prisma/client";

// for information about these interfaces
declare global {
	namespace App {
		interface Node {
			id: number;
			document_id: number;
			parent_id: number | null;
			topic_and_content: string;
		}

		// interface Error {}
		interface Locals {
			user: import("lucia").User | null;
			session: import("lucia").Session | null;
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	};

	// eslint-disable-next-line no-var
	var prismaClient: PrismaClient;
}

export { };
