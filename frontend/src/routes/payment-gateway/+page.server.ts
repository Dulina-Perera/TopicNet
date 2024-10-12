import { STRIPE_SECRET_KEY } from "$env/static/private";
import Stripe from "stripe";
import type { Actions } from "../$types";
import { error, redirect } from "@sveltejs/kit";

const stripe: Stripe = new Stripe(STRIPE_SECRET_KEY);

export const actions: Actions = {
	checkout: async ({ request }) => {
		let url: string | null;

		try {
			const session: Stripe.Response<Stripe.Checkout.Session> = await stripe.checkout.sessions.create({
				line_items: [
					{
						price: "price_1Q9BWLDYpXb80T0j1wILSdbw",
						quantity: 1,
					},
				],
				mode: "payment",
				success_url: `${request.headers.get("origin")}?success=true`,
				cancel_url: `${request.headers.get("origin")}?cancelled=true`,
			});

			url = session.url;
		} catch (errorObj) {
			throw error(500, errorObj as Error);
		}

		if (url) {
			throw redirect(303, url);
		}
	}
};
