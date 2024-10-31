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
	},

	login: async (event) => {
		const formData = await event.request.formData();
		const username = formData.get("username");
		const password = formData.get("password");

		if (
			typeof username !== "string" ||
			username.length < 3 ||
			username.length > 31 ||
			!/^[a-z0-9_-]+$/.test(username)
		) {
			return fail(400, {
				message: "Invalid username"
			});
		}

		if (typeof password !== "string" || password.length < 6 || password.length > 255) {
			return fail(400, {
				message: "Invalid password"
			});
		}

		const existingUser = await prismaClient.user.findUnique({
			where: { username: username.toLowerCase() }
		});
		if (!existingUser) {
			// NOTE:
			// Returning immediately allows malicious actors to figure out valid usernames from response times,
			// allowing them to only focus on guessing passwords in brute-force attacks.
			// As a preventive measure, you may want to hash passwords even for invalid usernames.
			// However, valid usernames can be already be revealed with the signup page among other methods.
			// It will also be much more resource intensive.
			// Since protecting against this is non-trivial,
			// it is crucial your implementation is protected against brute-force attacks with login throttling etc.
			// If usernames are public, you may outright tell the user that the username is invalid.
			return fail(400, {
				message: "Incorrect username or password"
			});
		}

		const validPassword = await bcrypt.compare(password, existingUser.passwordHash);
		if (!validPassword) {
			console.log("Yikes")
			return fail(400, {
				message: "Incorrect username or password"
			});
		}

		const session = await lucia.createSession(existingUser.id, {});
		const sessionCookie = lucia.createSessionCookie(session.id);
		event.cookies.set(sessionCookie.name, sessionCookie.value, {
			path: ".",
			...sessionCookie.attributes
		});

		redirect(302, "/");
	}
};
