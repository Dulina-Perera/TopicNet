import type { Actions, PageServerLoad } from "./$types";
import { prismaClient } from "$lib/server/prisma";
import { fail } from "@sveltejs/kit";

export const load: PageServerLoad = async () => {
	return {
		articles: await prismaClient.article.findMany()
	};
};

export const actions: Actions = {
	createArticle: async ({ request }) => {
		const { title, content } = Object.fromEntries(await request.formData()) as {
			title: string,
			content: string
		};

		try {
			await prismaClient.article.create({
				data: {
					title,
					content
				}
			});
		} catch (error) {
			console.error(error);
			return fail(500, { message: "Failed to create article" });
		}

		return {
			status: 201
		};
	},

	deleteArticle: async ({ url }) => {
		const id = url.searchParams.get("id");

		if (!id) {
			return fail(400, { message: "Missing id" });
		}

		try {
			await prismaClient.article.delete({
				where: {
					id: parseInt(id)
				}
			});
		} catch (error) {
			console.error(error);
			return fail(500, { message: "Failed to delete article" });
		};

		return {
			status: 200
		};
	}
};
