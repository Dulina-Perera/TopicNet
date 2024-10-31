import { error } from "@sveltejs/kit";
import type { PageServerLoad } from './$types';

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
