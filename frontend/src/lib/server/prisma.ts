// frontend/src/lib/server/prisma.ts

import { PrismaClient } from "@prisma/client";

const prismaClient = global.prismaClient || new PrismaClient();

if (process.env.NODE_ENV === "development") {
	global.prismaClient = prismaClient;
}

export { prismaClient };
