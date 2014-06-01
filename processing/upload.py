# CREATED: 6/1/14 3:58 PM by Justin Salamon <justin.salamon@nyu.edu>

import os, argparse

def upload(folder, user):

    server = "shell.cusp.nyu.edu:/scratch/www/files/sonyc/citizensound/"
    print "Uploading data to server..."
    command = "scp -r " + os.path.join(folder,"*") + " " + user + "@" + server
    os.system(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload files to server")
    parser.add_argument("folder", help="Path to folder folders to upload to server")
    parser.add_argument("user", help="Username on server")
    # parser.add_argument("jsonfolder", help="Path to folder to json file")

    args = parser.parse_args()
    if args.folder is not None:
        upload(args.folder, args.user)

    