import { Lucia } from "lucia";
import { PrismaAdapter } from "@lucia-auth/adapter-prisma";
import { dev } from "$app/environment";
import { prismaClient } from "$lib/server/prisma";

const adapter = new PrismaAdapter(prismaClient.session, prismaClient.user);

export const auth = new Lucia(adapter, {
	sessionCookie: {
		attributes: {
			secure: !dev,
		},
	},
	getUserAttributes: (attributes) => {
		return {
			userId: attributes.id,
			username: attributes.username,
		}
	}
});

export type Auth = typeof auth;
