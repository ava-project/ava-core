import os

LAMBDA = -1
WINDOWS_TARGET_EXTENSION = "exe"

#print(os.getenv('PATH'))

class FileCrawler(object):
    """
           FileCrawler :
           Used to find file amongst Path directories and custom directories
           trying to optimize the search
           instanced with a config file path for the custom directories
           call FileCrawler.locateExecutablePath() with full name
           or part name of the file to be found

           :param JSONData_file_preferences : A JSON Array containing path to
                                              user custom searchable directories

           :attr searching_depth : level of recursive search
    """

    def __init__(self, JSONData_file_preferences):
        super(FileCrawler, self).__init__()
        self._JSONData_file_preferences = JSONData_file_preferences
        self.customPaths = []
        self.TARGET_EXTENSION = WINDOWS_TARGET_EXTENSION
        self._searching_depth = 5

        self.__AddCustomsPaths()

    def __AddCustomsPaths(self):
        try:
            for entry in self._JSONData_file_preferences:
                self.customPaths.append(os.path.normpath(entry))
            # for entry in os.environ['PATH'].rsplit(';') :
            #     self.customPaths.append(entry);
        except:
            print("Error while adding folders to research list")

    def locateExecutablePath(self, TargetName):
        result = False

        for folder in self.customPaths:
            try:
                print("Searching " + folder)
                result = self.__Crawldir(folder, TargetName, 0, -1)
            except:
                print("UNEXPECTED Error")
            if result is not False:
                return result
        return result

    def __CertifyResult(self, fileItem, dirname, targetName):
        fd = os.path.join(dirname, fileItem)
        ok = False
        parsedFileItem = fileItem.lower().rsplit('.')
        prsdFILen = len(parsedFileItem)
        parsedTargetName = targetName.lower().rsplit('.')
        prsdTNLen = len(parsedTargetName)

        if prsdFILen > prsdTNLen + 1:
            return False

        if os.path.isfile(fd):
            if (prsdTNLen > 1) and (prsdFILen >= prsdTNLen):
                i = 0
                for value in parsedTargetName:
                    if value != parsedFileItem[i]:
                        return False
                    i += 1
                if parsedFileItem[prsdFILen - 1] == self.TARGET_EXTENSION or parsedFileItem[prsdFILen - 1] == "":
                    return fd

            elif (parsedFileItem[0] == targetName.lower()) and (parsedFileItem[prsdFILen - 1] == self.TARGET_EXTENSION):
                return fd

            elif (parsedFileItem[0] == targetName.lower()) and parsedFileItem[prsdFILen - 1] == "lnk":
                return fd

        # if (os.path.isfile(fd)) and (parsedFileItem[0] == targetName.lower()) and (len(parsedFileItem) > 1):
        #     if (parsedFileItem[prsdFILen - 1] == self.TARGET_EXTENSION):
        #         return fd
        #     if (prsdFILen == prsdTNLen) and (parsedFileItem[prsdFILen - 1] == parsedTargetName[prsdTNLen - 1]):
        #         return fd
        return False

        # fd = os.path.join(dirname, fileItem)
        # parsedFileItem = fileItem.lower().rsplit('.')
        # parsedTargetName = targetName.lower.rsplit('.')
        # # prsdFILen = len(parsedFileItem)
        # # prsdTNLen = len(parsedTargetName)
        # if (os.path.isfile(fd)) and (parsedFileItem[0] == targetName.lower()) and (len(parsedFileItem) > 1):
        #     if (parsedFileItem[prsdFILen - 1] == self.TARGET_EXTENSION):
        #         return fd
        #     # if (prsdFILen == prsdTNLen) and (parsedFileItem[prsdFILen - 1] == parsedTargetName[prsdTNLen - 1]):
        #         # return fd
        # return False

    def __EvalLocalFiles(self, dirname, targetName):
        """
        Search recursively for [targetName{.exe}] from [dirname] with a maximum depth of [depth]
        if it is likely the for the target to be found in current folder or subfolder,
        starts by looking for files, then by subfolders containing targetName in their name
        then trying toher subfolders until depth max is reached.
        """
        result = False
        for fileItem in os.listdir(dirname):
            result = self.__CertifyResult(fileItem, dirname, targetName)
            if result is not False:
                break
        return result


    def __Crawldir(self, dirname, targetName, depth, likelihood=LAMBDA):
        localdepth = depth + 1
        result = False
        if likelihood > LAMBDA:
            result = self.__EvalLocalFiles(dirname, targetName)
            if result is not False:
                return result
        try:
            """
            Exceptions here as windows admin rights on a folder across the search make it stop premeturely
            to be looked for later as windows processes run by group
            likely, the daemon would be run as admin.
            We first try to find subfolders likely to host the target and start with them
            """
            for subfolderItem in os.listdir(dirname):
                if (os.path.isdir(os.path.join(dirname, subfolderItem)) and (os.access(os.path.join(dirname, subfolderItem), os.R_OK))):
                    sublikelihood = self.__evalLikeliHood(os.path.join(dirname, subfolderItem), targetName)
                    if sublikelihood > LAMBDA:
                        result = self.__Crawldir(os.path.join(dirname, subfolderItem), targetName, localdepth, sublikelihood)
                        if result is not False:
                            return result
            if likelihood == LAMBDA:
                result = self.__EvalLocalFiles(dirname, targetName)
                if result is not False:
                    return result
        except:
            pass
        try:
            """
            If the previous step has failed we try all subfolders excluding those previously tested
            """
            for subfolderItem in os.listdir(dirname):
                if os.path.isdir(os.path.join(dirname, subfolderItem)):
                    sublikelihood = self.__evalLikeliHood(os.path.join(dirname, subfolderItem), targetName)
                    if (sublikelihood == LAMBDA) and (depth < self._searching_depth):
                        result = self.__Crawldir(os.path.join(dirname, subfolderItem), targetName, localdepth, sublikelihood)
                        if result != False:
                            return result
        except:
            pass
        return result

    def __evalLikeliHood(self, dirname, targetName):
        target = targetName.rsplit('.')[0]
        return dirname.lower().find(target.lower())


    def set_searching_depth(self, searching_depth):
        self._searching_depth = 0 if searching_depth < 0 else searching_depth

# def main():
# #     print(sys.argv)
#     FileProbe = FileCrawler("C:\\Users\\Jamais\\ava-core\\Windows_cross\\Config\\FileCrawler\\FilePreference.config")
# #     flocation = FileProbe.locateExecutablePath("Chrome")
#     flocation = False
#     if (len(sys.argv) > 1):
#         flocation = FileProbe.locateExecutablePath(str(sys.argv[1]))
#     if (flocation != False):
#         useranswer = input("\n\nExecute " + flocation + " ? (y/n)\n>  ")
#         if (useranswer == "y") or (useranswer == "yes"):
#             subprocess.Popen(   flocation,
#                             stdout=subprocess.PIPE,
#                             stderr=subprocess.STDOUT,
#                             stdin=PIPE,
#                             shell=False,
#                             bufsize=0)
#     else:
#         print("Sorry, no result found")
# # #    FileProbe.test()
#
# if __name__ == "__main__":
#     main()
