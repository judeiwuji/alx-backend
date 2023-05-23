import { createClient } from "redis";

const main = async () => {
  const client = createClient();
  client.on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err.message}`)
  );

  client.on("connect", (err) =>
    console.log("Redis client connected to the server")
  );
};

main();
