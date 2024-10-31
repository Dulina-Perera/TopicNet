import type { Actions, PageServerLoad } from "./$types";
import { Cookie } from "lucia";
import { error } from "@sveltejs/kit";
import { fail, redirect } from "@sveltejs/kit";
import { lucia } from "$lib/server/lucia";

export const load: PageServerLoad = async ({ parent, params }) => {
	const parentData = await parent();

	const response = await fetch(`http://localhost:5000/api/v1/download/nodes?document_id_=${params.document_id}`);
	if (!response.ok) {
		throw error(404, "Failed to fetch nodes");
	}

	const nodes = await response.json();

	return {
		...parentData,
		nodes,
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
