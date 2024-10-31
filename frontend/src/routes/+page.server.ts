import bcrypt from "bcrypt";
import type { Actions, PageServerLoad } from "./$types";
import { fail, redirect } from "@sveltejs/kit";
import { Cookie } from "lucia";
import { lucia } from "$lib/server/lucia";
import { prismaClient } from "$lib/server/prisma";

export const load: PageServerLoad = async ({ locals }) => {
	return {
		user: locals.user
	};
};

export const actions: Actions = {
	logout: async ({ locals, cookies }) => {
		if (!locals.session) {
			return fail(401);
		}

		await lucia.invalidateSession(locals.session.id);

		const sessionCookie: Cookie = lucia.createBlankSessionCookie();
		cookies.set(sessionCookie.name, sessionCookie.value, {
			path: "/",
			...sessionCookie.attributes
		});

		throw redirect(302, "/?loggedOut=true");
	}
};
