import { Lucia, TimeSpan } from "lucia";
import { PrismaAdapter } from "@lucia-auth/adapter-prisma";
import type { PrismaClient, User } from "@prisma/client";
import { dev } from "$app/environment";
import { prismaClient } from "$lib/server/prisma";

const adapter: PrismaAdapter<PrismaClient> = new PrismaAdapter(prismaClient.session, prismaClient.user);

export const lucia: Lucia<Record<never, never>, {
	userId: string;
	username: string;
	isPermanent: boolean;
}> = new Lucia(adapter, {
	getUserAttributes: (attributes: Partial<User>) => {
		return {
			username: attributes.username as string,
			isPermanent: attributes.isPermanent as boolean
		}
	},
	sessionCookie: {
		attributes: {
			secure: !dev,
		},
	},
	sessionExpiresIn: new TimeSpan(2, "w")
});

export type Auth = typeof lucia;
