import { Job, Queue } from "kue";

/**
 * @param {*[]} jobs
 * @param {Queue} queue
 */
const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error("Jobs is not an array");
  }

  for (const data of jobs) {
    const job = queue.create("push_notification_code_3", data).save((err) => {
      if (err) {
        return console.log(`Notification job JOB_ID failed: ${err.message}`);
      }
      console.log(`Notification job created: ${job.id}`);
    });

    job.on("complete", () => {
      console.log(`Notification job ${job.id} completed`);
    });

    job.on("progress", (progress, data) => {
      console.log(`Notification job JOB_ID ${progress}% complete`);
    });
  }
};

export default createPushNotificationsJobs;
