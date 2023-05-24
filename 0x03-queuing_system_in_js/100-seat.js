import express from "express";
import redis from "redis";
import { promisify } from "util";
import kue from "kue";

const client = redis.createClient();
const app = express();
const PORT = 1245;
const queue = kue.createQueue();
let reservationEnabled = true;

client.on("error", (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

function reserveSeat(number) {
  client.set("available_seats", number);
}

async function getCurrentAvailableSeats() {
  const get = promisify(client.get).bind(client);
  const available_seats = await get("available_seats");
  return available_seats ? parseInt(available_seats) : 0;
}

app.get("/available_seats", async (req, res) => {
  const seats = await getCurrentAvailableSeats();

  res.send({ numberOfAvailableSeats: `${seats}` });
});

app.get("/reserve_seat", async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  if (!reservationEnabled) {
    return res.send({ status: "Reservation are blocked" });
  }

  const job = queue.create("reserve_seat", {});
  job.save((err) => {
    if (err) {
      return res.send({ status: "Reservation failed" });
    }
    res.send({ status: "Reservation in process" });
  });

  job.on("complete", () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on("failed", (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get("/process", async (req, res) => {
  queue.process("reserve_seat", async (job, done) => {
    const availableSeats = (await getCurrentAvailableSeats()) - 1;
    if (availableSeats < 0) {
      return done(new Error("Not enough seats available"));
    }
    reserveSeat(availableSeats);
    if (availableSeats === 0) {
      reservationEnabled = false;
    }
    done();
  });
  res.send({ status: "Queue processing" });
});

app.listen(PORT, () => {
  console.log("Server is online");
  reserveSeat(50);
});
