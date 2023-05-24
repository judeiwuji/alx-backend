import express from "express";
import redis from "redis";
import { promisify } from "util";

const client = redis.createClient();
const app = express();
client.on("error", (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});
client.on("connect", () => {
  console.log("Redis client connected to the server");
});
const listProducts = [
  { id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { id: 4, name: "Suitcase 1050", price: 550, stock: 5 },
];

function getItemById(id) {
  return listProducts.find((d) => d.id === id);
}

function reserveStockById(itemId, stock) {
  client.set(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  const get = promisify(client.get).bind(client);
  const stock = await get(itemId);
  return stock ? parseInt(stock) : 0;
}

app.get("/list_products", async (req, res) => {
  const products = listProducts.map(async (d) => {
    const stock = await getCurrentReservedStockById(d.id);
    return {
      itemId: d.id,
      itemName: d.name,
      price: d.price,
      initialAvailableQuantity: d.stock - stock,
      currentQuantity: d.stock,
    };
  });
  res.send(await Promise.all(products));
});

app.get("/list_products/:itemId(\\d+)", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = listProducts.find((d) => d.id === itemId);
  const stock = await getCurrentReservedStockById(itemId);
  if (item) {
    return res.send({
      itemId: item.id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock - stock,
      currentQuantity: item.stock,
    });
  }
  res.send({ status: "Product not found" });
});

app.get("/reserve_product/:itemId(\\d+)", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = listProducts.find((d) => d.id === itemId);
  const stock = await getCurrentReservedStockById(itemId);

  if (!item) {
    return res.send({ status: "Product not found" });
  }

  if (item.stock - stock === 0) {
    return res.send({ status: "Not enough stock available", itemId });
  }
  reserveStockById(itemId, stock + 1);
  res.send({ status: "Reservation confirmed", itemId });
});

app.listen(1245, () => console.log("Server online"));
