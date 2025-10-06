import Fastify from "fastify";
import mysql from "mysql2/promise";
import healthRoutes from "./routes/health.js";

const fastify = Fastify({
  logger: true,
});

// Criar pool de conexões com MySQL
const db = await mysql.createPool({
  host: "db", // nome do serviço no docker-compose
  user: "segueoplano_user",
  password: "segueoplano_pass",
  database: "segueoplano_db",
});

// Disponibilizar o DB no Fastify
fastify.decorate("db", db);

// Rotas
fastify.register(healthRoutes);

// Inicializa servidor
const start = async () => {
  try {
    await fastify.listen({ port: 3000, host: "0.0.0.0" });
    fastify.log.info(`🚀 Server ready at http://localhost:3000`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
