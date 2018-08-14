import argparse, os, sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ifile', help = 'Input file name', required = True)
    parser.add_argument('-o', '--ofile', help = 'Output file name' , required = True)
    args = parser.parse_args()

    if(os.path.isfile(args.ifile)):
        with open(args.ifile, 'r') as fi:
            inputArgs = fi.readlines()
        fi.close()
    else:
        print 'File does not exist'
        sys.exit()

    with open(args.ofile, 'w') as fo:
        for arg in filter(lambda i: ',' in i, inputArgs):
            keyVal = arg.split(',')

            sqlInsert = "[" + keyVal[1].rstrip() + ", " + keyVal[0].rstrip() + "],\n"
            fo.write(sqlInsert)
    fo.close()

    print 'Successful: ' + args.ofile

if __name__ == "__main__":
    main()
