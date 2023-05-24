import { createClient } from "redis";
import { promisify } from "util";

const client = createClient();
const main = async () => {
  client.on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err.message}`)
  );

  client.on("connect", (err) =>
    console.log("Redis client connected to the server")
  );
};

const setNewSchool = (schooolName, value) => {
  client.set(schooolName, value, (err, reply) => {
    if (err) {
      return console.log(err.message);
    }
    console.log(`Reply: ${reply}`);
  });
};

const displaySchoolValue = async (schooolName) => {
  const get = promisify(client.get).bind(client);
  const reply = await get(schooolName);
  console.log(reply);
};

main();
displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");
