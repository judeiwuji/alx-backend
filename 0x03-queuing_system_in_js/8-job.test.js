import kue from "kue";
import { expect } from "chai";
import createPushNotificationsJobs from "./8-job";
const queue = kue.createQueue();

describe("createPushNotificationsJobs", () => {
  before(function () {
    queue.testMode.enter();
  });

  afterEach(function () {
    queue.testMode.clear();
  });

  after(function () {
    queue.testMode.exit();
  });

  it("should display a error message if jobs is not an array", function () {
    expect(function () {
      createPushNotificationsJobs(null, queue);
    }).to.throw("Jobs is not an array");
  });

  it("should create two new jobs to the queue", () => {
    createPushNotificationsJobs(
      [
        {
          phoneNumber: "test-4153518780",
          message: "test data",
        },
        {
          phoneNumber: "test-4153518781",
          message: "test data 1",
        },
      ],
      queue
    );

    expect(queue.testMode.jobs.length).to.equal(2);
  });

  it("should have a new job with phone number test-4153", () => {
    createPushNotificationsJobs(
      [
        {
          phoneNumber: "test-4153",
          message: "test data",
        },
      ],
      queue
    );

    expect(queue.testMode.jobs[0].data.phoneNumber).to.equal("test-4153");
  });

  it("should have a new job with message testing", () => {
    createPushNotificationsJobs(
      [
        {
          phoneNumber: "test-41530",
          message: "testing",
        },
      ],
      queue
    );

    expect(queue.testMode.jobs[0].data.message).to.equal("testing");
  });
});
