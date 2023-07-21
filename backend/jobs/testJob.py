from backend.jobs.BasicJob import BasicJob


# class TestJob (BasicJob):
#
#
# if __name__ == "__main__":
#     print("runnig")
#     TestJob("test job").runJob()
#     print("done")


def runJob():
    f = open("demofile2.txt", "a")
    f.write("Job is running \n")
    # f.write(self.getJobDetails())
    f.close()