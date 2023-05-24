import { createClient } from "redis";

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

const displaySchoolValue = (schooolName) => {
  client.get(schooolName, (err, reply) => {
    if (err) {
      return console.log(err.message);
    }

    console.log(reply);
  });
};

main();
displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");
