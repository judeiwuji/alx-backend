import kue from "kue";

const queue = kue.createQueue();
const jobData = {
  phoneNumber: "090350098800",
  message: "publish app to prod",
};
const job = queue.create("push_notification_code", jobData).save((err) => {
  if (err) {
    return console.log("Notification job failed");
  }
  console.log(`Notification job created: ${job.id}`);
});

job.on("complete", () => {
  console.log("Notification job completed");
});
