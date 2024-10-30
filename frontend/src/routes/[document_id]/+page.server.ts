import { error } from "@sveltejs/kit";

export async function load({ params }) {
	async function getNodes() {
		const response: Response = await fetch(`http://localhost:5000/api/v1/download/nodes?document_id_=${params.document_id}`);

		if (!response.ok) {
			throw error(404, "Failed to fetch nodes");
		}

		return await response.json();
	}

	return {
		nodes: await getNodes()
	};
}
