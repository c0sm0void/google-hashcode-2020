#coding=utf-8
#!/bin/python3

SEP = "/"
INPUT_DATA_FOLDER = "library-in-files"
INPUT_DATA_FILES = [
    "a_example",  # 7 days
    "e_so_many_books",  # 200 days
    "f_libraries_of_the_world"  # 700 days
    "b_read_on",  # 1000 days
    "d_tough_choices",  # 30001 days
    "c_incunabula",  # 100000 days
]
INPUT_DATA_EXT = ".txt"
OUTPUT_DATA_DIR = "out"
OUTPUT_DATA_EXT = ".out"


def importProblemStatement():
    for fileBase in INPUT_DATA_FILES:
        with open(INPUT_DATA_FOLDER + SEP + fileBase + INPUT_DATA_EXT, "r") as f:
            outputFile = OUTPUT_DATA_DIR + SEP + fileBase + OUTPUT_DATA_EXT

            meta, libraries = parseProblemStatement(f)

            #print('Parsed problem statement ({}):\n'.format(fileBase), meta, '\n', libraries)

            registeredLibs = signupLibsAndScanBooks(meta, libraries)

            #print('Registered libs done scanning:\n', registeredLibs)

            output = parseOutputAndWriteToFile(registeredLibs)
            saveOutput(outputFile, output)


def saveOutput(fileLocation, data):
    with open(fileLocation, "w+") as f:
        f.write(data)


def parseOutputAndWriteToFile(registeredLibs):
    output = ""

    # lib count
    output += str(len(registeredLibs)) + "\n"

    for lib in registeredLibs:
        output += str(lib['id']) + " " + str(len(lib['booksScanned'])) + "\n"
        for book in lib['booksScanned']:
            output += str(book['bookid']) + ' '
        output += '\n'

    return output


def orderLibsByValue(libraries):
    valuedLibs = []

    for lib in libraries:
        lib['libScore'] = \
                      (int(lib['booksShippingPerDay']) \
                       * int(lib['booksCount'])) \
                    - (int(lib['booksShippingPerDay']) \
                       * int(lib['signupDays']))

        valuedLibs += [lib]

    sorted(valuedLibs, key = lambda libz: int(libz['libScore']))

    # print("DEBUG: valuedLibs", valuedLibs)

    return valuedLibs


def signupLibsAndScanBooks(meta, libraries):

    # Best library (highest throughput)
    # rank all libs order by highest <value>
    libs = orderLibsByValue(libraries)

    registeredLibs = []
    inLibraryRegisteringProcess = False

    alreadyScannedBookIds = []

    for day in range(int(meta['days'])):
        print("Day {}/{}".format(day, meta['days']))

        if not (len(registeredLibs)) == 0:  # unregister possibly
            #print("DEBUG registered:", registeredLibs[-1], day, isRegistered(registeredLibs[-1], day))

            if isRegistered(registeredLibs[-1], day):
                inLibraryRegisteringProcess = False

        if not inLibraryRegisteringProcess and len(libs) > 0:  # investigate last lib OR len = 0
            inLibraryRegisteringProcess = True
            chosenLib = libs.pop(0)
            registeredLibs += [chosenLib]  # nextBestLib
            chosenLib['signupStarted'] = day

        for lib in allLibsDoneRegistering(registeredLibs, day):
            for capacity in range(int(lib['booksShippingPerDay'])):
                bookToScan = getHighestValueBookNotYetScanned(lib, alreadyScannedBookIds)

                if bookToScan is not None:

                    lib['booksScanned'] += [bookToScan]
                    alreadyScannedBookIds += [bookToScan['bookid']]

    return registeredLibs  # abzüglich die die noch nicht fertig regoistriert sind!!!!


def getHighestValueBookNotYetScanned(lib, alreadyScannedBookIds):
    for book in lib['bookIds']:
        if not int(book['bookid']) in alreadyScannedBookIds:
            lib['bookIds'] = lib['bookIds'][1:]
            return book
    return None


def allLibsDoneRegistering(registeredLibs, currentDay):
    successfullyRegisteredLibs = []

    for lib in registeredLibs:
        if isRegistered(lib, currentDay):
            successfullyRegisteredLibs += [lib]

    return successfullyRegisteredLibs


def isRegistered(lib, day):
    return int(lib['signupStarted']) + int(day) >= int(lib['signupDays'])


def orderBooksByAndEnrichWithScore(bookIds, metaData):
    possibleBooks = []

    for book in bookIds:
        possibleBooks += [{'bookid': int(book), 'bookScore': metaData['bookScores'][int(book)]}]

    possibleBooks.sort(key = lambda b: b['bookScore'], reverse=True)

    if len(possibleBooks) > 1:
        return possibleBooks
    else:
        return []


def parseProblemStatement(problemFile):
    line1 = problemFile.readline().replace('\n', '')
    numberOfBooks, numberOfLibs, days = line1.split(' ')

    line2 = problemFile.readline().replace('\n', '')
    bookScores = line2.split(' ')

    meta = {'days': days, 'bookScores': bookScores}

    libraries = []

    for lib in range(int(numberOfLibs)):
        library = {'id': lib}
        libLine1 = problemFile.readline().replace('\n', '').split(' ')
        libLine2 = problemFile.readline().replace('\n', '').split(' ')

        library['booksCount'] = libLine1[0]
        library['signupDays'] = libLine1[1]
        library['booksShippingPerDay'] = libLine1[2]
        library['bookIds'] = orderBooksByAndEnrichWithScore(libLine2, meta)

        library['booksScanned'] = []

        libraries += [library]

    return meta, libraries


if __name__ == "__main__":
    importProblemStatement()
