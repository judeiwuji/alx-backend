import { createClient, print } from "redis";
import { promisify } from "util";

const client = createClient();
const main = async () => {
  client.on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err.message}`)
  );

  client.on("connect", (err) =>
    console.log("Redis client connected to the server")
  );

  client.hset("HolbertonSchools", "Portland", 50, (err, reply) => {
    print(err, reply);
  });

  client.hset("HolbertonSchools", "Seattle", 80, (err, reply) => {
    print(err, reply);
  });

  client.hset("HolbertonSchools", "New York", 20, (err, reply) => {
    print(err, reply);
  });

  client.hset("HolbertonSchools", "Bogota", 20, (err, reply) => {
    print(err, reply);
  });

  client.hset("HolbertonSchools", "Cali", 40, (err, reply) => {
    print(err, reply);
  });

  client.hset("HolbertonSchools", "Paris", 2, (err, reply) => {
    print(err, reply);
  });

  client.hgetall("HolbertonSchools", (err, reply) => {
    print(err, JSON.stringify(reply, null, 2));
  });
};

main();
