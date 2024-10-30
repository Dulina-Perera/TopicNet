import bcrypt from "bcrypt";
import type { Actions } from "./$types";
import { fail, redirect } from "@sveltejs/kit";
import { Cookie, generateIdFromEntropySize } from "lucia";
import { lucia } from "$lib/server/lucia";
import { prismaClient } from "$lib/server/prisma";
import type { Session } from "@prisma/client";

export const actions: Actions = {
	register: async (event) => {
		const formData = await event.request.formData();
		console.log(formData);
		const username = formData.get("username");
		const password = formData.get("password");

		if (
			typeof username !== "string" ||
			username.length < 4 ||
			username.length > 30 ||
			!/^[a-z0-9-_]+$/.test(username)
		) {
			return fail(400, {
				message: "Username must be 4-30 characters, containing only lowercase letters, numbers, dashes, or underscores."
			});
		}

		if (typeof password !== "string" || password.length < 16 || password.length > 64) {
			return fail(400, {
				message: "Password must be between 16 and 64 characters."
			});
		}

		const userId = generateIdFromEntropySize(10);
		const passwordHash = await bcrypt.hash(password, 10);

		const existingUser = await prismaClient.user.findUnique({ where: { username } });
		if (existingUser) {
			return fail(400, {
				message: "Username already taken. Please choose another one."
			});
		}

		await prismaClient.user.create({
			data: { id: userId, username, passwordHash, isPermanent: true }
		});

		const session: Session = await lucia.createSession(userId, {});
		const sessionCookie: Cookie = lucia.createSessionCookie(session.id);
		event.cookies.set(sessionCookie.name, sessionCookie.value, {
			path: ".",
			...sessionCookie.attributes
		});

		throw redirect(302, "/");
	}
};
