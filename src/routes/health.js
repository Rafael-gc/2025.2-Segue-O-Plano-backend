export default async function healthRoutes(fastify, options) {
  fastify.get("/health", async () => {
    try {
      const [rows] = await fastify.db.query("SELECT 1 + 1 AS result");
      return { status: "ok", db: rows[0].result, message: "API is running 🚀" };
    } catch (err) {
      return { status: "error", message: "Database connection failed ❌", error: err.message };
    }
  });
}
