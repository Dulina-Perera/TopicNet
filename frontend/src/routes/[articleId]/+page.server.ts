import type { Actions, PageServerLoad } from "../$types";
import { error, fail } from "@sveltejs/kit";

import { prismaClient } from "$lib/server/prisma";

export const load: PageServerLoad = async ({ params }) => {
	const getArticle = async () => {
		const article = await prismaClient.article.findUnique({
			where: {
				id: parseInt(params.articleId)
			}
		});

		if (!article) {
			throw error(404, "Article not found");
		}
		return article;
	}

	return {
		article: await getArticle()
	};
};

export const actions: Actions = {
	updateArticle: async ({ request, params }) => {
		const { title, content } = Object.fromEntries(await request.formData()) as {
			title: string,
			content: string
		};

		try {
			await prismaClient.article.update({
				where: {
					id: parseInt(params.articleId)
				},
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
			status: 200
		};
	},
};
